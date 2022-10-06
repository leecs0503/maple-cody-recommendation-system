import logging
import random
import os
from ..server.config import Config
from ..Avatar.avatar import Avatar
from .WCR_caller import WCRCaller
from PIL import Image
from typing import List, Tuple
import base64
import io


def is_pixel_eq(
    a: Tuple[int, int, int, int],
    b: Tuple[int, int, int, int],
):
    return abs(a[0] - b[0]) < 8 and abs(a[1] - b[1]) < 8 and abs(a[2] - b[2]) < 8 and abs(a[3] - b[3]) < 8


class ImageProcessor:
    def __init__(
        self,
        logger: logging.Logger,
        config: Config,
    ):
        self.logger = logger
        self.caller = WCRCaller(
            logger=self.logger,
            wcr_server_host=config.wcr_server_host,
            wcr_server_protocol=config.wcr_server_protocol,
            wcr_server_port=config.wcr_server_port,
            retry_num=config.wcr_caller_retry_num,
            timeout=config.wcr_caller_timeout,
            backoff=config.wcr_caller_backoff,
        )
        self.item_code_list = []

    async def _naive_approach(
        item_coord,
    ):
        # TODO:
        """
        SAMPLE_SIZE = 500
        AVATAR_COORD_RATIO = 1

        sample_pix_coord = random.sample(item_coord, min(len(item_coord), SAMPLE_SIZE))

        prob_compare = []
        for rows in sample_row_coord:
            cnt = 0
            for cols in sample_col_coord:
                cnt = 0
                for compare_rows, compare_cols in sample_pix_coord:
                    av_rgba = image_avatar.getpixel((rows + compare_rows, cols + compare_cols))
                    item_rgba = image_item.getpixel((compare_rows, compare_cols))
                    if (
                        (av_rgba[0] == item_rgba[0])
                        and (av_rgba[1] == item_rgba[1])
                        and (av_rgba[2] == item_rgba[2])
                    ):
                        cnt += 1
                else:
                    prob = cnt / len(sample_pix_coord)
                    prob_compare.append(prob)
        else:
            maximum = max(prob_compare)
            print("accuracy : ", maximum)
        return maximum
        """

    def _correct_visualize(self, base_image: Image.Image, test_image: Image.Image):
        base_uri = os.path.dirname(__file__)

        acc, px, py = self.is_contain(base_image, test_image)
        test_format = base_image.copy()
        (h, w) = test_image.size
        pixels = test_format.load()
        for x in range(h):
            for y in range(w):
                ax, ay = (px + x, py + y)
                pa = base_image.getpixel((ax, ay))
                ta = test_image.getpixel((x, y))
                if not is_pixel_eq(pa, ta):
                    # pixels[ax, ay] = (255 - pixels[ax, ay][0] , 255 - pixels[ax, ay][1], 255 - pixels[ax, ay][2], pixels[ax, ay][3])
                    pixels[ax, ay] = (100, 100, 100, pixels[ax, ay][3])

        visualize_path = os.path.join(base_uri, "correct_visualize", "visualize.png")

        test_format.save(visualize_path)
        print(f"original - made acc: {acc}")
        return acc

    def _get_sample_pixel_list(
        self,
        image: Image.Image,
        sample_size: int,
    ):
        [height, width] = image.size
        item_coord = []
        num_item_pixel = 0
        for row in range(height):
            for col in range(width):
                alpha = image.getpixel((row, col))[3]
                if alpha != 0:
                    num_item_pixel += 1
                    item_coord.append((row, col))
        if 0 <= num_item_pixel <= 1:
            return -1

        assert num_item_pixel > 0

        sample_num = min(num_item_pixel, sample_size)
        return random.sample(item_coord, sample_num)

    def _get_ratio(
        self,
        pivot_row: int,
        pivot_col: int,
        avatar_image: Image.Image,
        item_image: Image.Image,
        xy_list: List[Tuple[int, int]],
    ):
        [avatar_height, avatar_width] = avatar_image.size

        correct_count = 0
        all_count = 0
        for (dx, dy) in xy_list:
            x = pivot_row + dx
            y = pivot_col + dy
            item_pixel = item_image.getpixel((dx, dy))
            item_alpha = item_pixel[3]
            if item_alpha == 0:
                continue
            if x >= avatar_height or y >= avatar_width:
                all_count += 1
                continue
            avatar_pixel = avatar_image.getpixel((x, y))
            if is_pixel_eq(avatar_pixel, item_pixel):
                correct_count += 1
            all_count += 1
        ratio = correct_count / all_count
        return ratio

    def is_contain(
        self,
        avatar_image: Image.Image,
        item_image: Image.Image,
    ) -> bool:
        """
        image_avatar:
        image_item:
        """
        SAMPLE_SIZE = 10
        VALIDATE_SAMPLE_NUM = 3

        [item_height, item_width] = item_image.size
        [avatar_height, avatar_width] = avatar_image.size

        sample_item_pixel_xy_list = self._get_sample_pixel_list(item_image, SAMPLE_SIZE)

        if sample_item_pixel_xy_list == -1:
            return (0, 0, 0)

        all_item_pixel_xy_list = [(x, y) for x in range(0, item_height) for y in range(0, item_width)]

        pivot_data = []
        for pivot_row in range(avatar_height):
            for pivot_col in range(avatar_width):
                ratio = self._get_ratio(
                    pivot_row=pivot_row,
                    pivot_col=pivot_col,
                    avatar_image=avatar_image,
                    item_image=item_image,
                    xy_list=sample_item_pixel_xy_list,
                )
                pivot_data.append((ratio, pivot_row, pivot_col))
        data = sorted(pivot_data, reverse=True)

        result = []
        for i in range(min(VALIDATE_SAMPLE_NUM, len(data))):
            (ratio, pivot_row, pivot_col) = data[i]
            correct_ratio = self._get_ratio(
                pivot_row=pivot_row,
                pivot_col=pivot_col,
                avatar_image=avatar_image,
                item_image=item_image,
                xy_list=all_item_pixel_xy_list,
            )
            result.append((correct_ratio, pivot_row, pivot_col))
        return sorted(result, reverse=True)[0]

    async def infer_sub(self, image: Image.Image, avatar: Avatar, code_idx: int) -> int:

        wcr_response = await self.caller.get_image(avatar=avatar)
        if wcr_response is None:
            return ((0, 0, 0), 0)

        image_data = base64.b64decode(wcr_response)
        item_image = Image.open(io.BytesIO(image_data))
        acc = self.is_contain(avatar_image=image, item_image=item_image), code_idx
        print("code_idx :", code_idx)
        print("acc:", acc)
        print("ㅡㅡㅡㅡㅡㅡㅡㅡ")
        return acc

    async def max_acc_code(self, acc_list: List) -> int:
        max_acc = 0
        for idx in range(len(acc_list)):
            print(acc_list[idx][0][0])
            if acc_list[idx][0][0] >= max_acc:
                max_acc = acc_list[idx][0][0]
                max_idx_acc = acc_list[idx][1]
        return max_idx_acc

    async def infer(self, image: Image) -> Avatar:
        # TODO: implement
        NUM_FACE = 20000
        NUM_CAP = 1004999
        NUM_LONGCOAT = 1052975
        NUM_WEAPON = 1703238
        NUM_COMPARE = 50

        acc_list = []
        for code_idx in range(NUM_FACE - NUM_COMPARE, NUM_FACE + NUM_COMPARE):
            avatar = Avatar(f"{code_idx}", "0", "0", "0")
            acc = await self.infer_sub(image=image, avatar=avatar, code_idx=code_idx)
            acc_list.append(acc)
        max_face_idx = await self.max_acc_code(acc_list)

        acc_list = []
        for code_idx in range(NUM_CAP - NUM_COMPARE, NUM_CAP + NUM_COMPARE):
            avatar = Avatar("0", f"{code_idx}", "0", "0")
            acc = await self.infer_sub(image=image, avatar=avatar, code_idx=code_idx)
            acc_list.append(acc)
        max_cap_idx = await self.max_acc_code(acc_list)

        acc_list = []
        for code_idx in range(NUM_LONGCOAT - NUM_COMPARE, NUM_LONGCOAT + NUM_COMPARE):
            avatar = Avatar("0", "0", f"{code_idx}", "0")
            acc = await self.infer_sub(image=image, avatar=avatar, code_idx=code_idx)
            acc_list.append(acc)
        max_longcoat_idx = await self.max_acc_code(acc_list)

        acc_list = []
        for code_idx in range(NUM_WEAPON - NUM_COMPARE, NUM_WEAPON + NUM_COMPARE):
            avatar = Avatar("0", "0", "0", f"{code_idx}")
            acc = await self.infer_sub(image=image, avatar=avatar, code_idx=code_idx)
            acc_list.append(acc)
        max_weapon_idx = await self.max_acc_code(acc_list)

        return Avatar(f"{max_face_idx}", f"{max_cap_idx}", f"{max_longcoat_idx}", f"{max_weapon_idx}")
