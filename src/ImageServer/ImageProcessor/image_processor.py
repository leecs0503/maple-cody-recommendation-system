import logging
import random
import os
from heapq import heappush, heappop
from ..server.config import Config
from ..Avatar.avatar import Avatar
from .WCR_caller import WCRCaller
from PIL import Image
from typing import List, Tuple, Optional
import base64
import io


PIXEL = Tuple[int, int, int, int]


def is_pixel_eq(
    a: PIXEL,
    b: PIXEL,
):
    return abs(a[0] - b[0]) < 8 and \
           abs(a[1] - b[1]) < 8 and \
           abs(a[2] - b[2]) < 8 and \
           abs(a[3] - b[3]) < 8


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
                    # pixels[ax, ay] = (
                    #     255 - pixels[ax, ay][0],
                    #     255 - pixels[ax, ay][1],
                    #     255 - pixels[ax, ay][2],
                    #     pixels[ax, ay][3]
                    # )
                    pixels[ax, ay] = (100, 100, 100, pixels[ax, ay][3])

        visualize_path = os.path.join(base_uri, "correct_visualize", "visualize.png")

        test_format.save(visualize_path)
        print(f"original - made acc: {acc}")
        return acc

    def _get_pixel_list(
        self,
        pixel_data: List[PIXEL],
        height: int,
        width: int,
    ):
        item_coord = [(idx % height, idx // height, pixel) for idx, pixel in enumerate(pixel_data) if pixel[3] != 0]
        num_item_pixel = len(item_coord)

        # PIXEL 크기 1인 이미지는 is_contained 로직으로 판단하기 어렵기 때문에,
        # 1 pixel인 경우도 빈 리스트를 반환.
        if num_item_pixel <= 1:
            return []

        assert num_item_pixel > 0
        return item_coord

    def _get_ratio(
        self,
        pivot_row: int,
        pivot_col: int,
        avatar_pixel_data: List[PIXEL],
        avatar_height: int,
        avatar_width: int,
        xy_list: List[Tuple[int, int, PIXEL]],
    ):
        correct_count = 0
        for dx, dy, item_pixel in xy_list:
            x = pivot_row + dx
            y = pivot_col + dy
            if x >= avatar_height or y >= avatar_width:
                continue
            avatar_pixel = avatar_pixel_data[y * avatar_height + x]
            if is_pixel_eq(avatar_pixel, item_pixel):
                correct_count += 1

        ratio = correct_count / len(xy_list)
        return ratio

    def is_contain(
        self,
        avatar_pixel_list: List[PIXEL],
        avatar_size: Tuple[int, int],
        item_pixel_list: List[PIXEL],
        item_size: Tuple[int, int],
    ) -> Tuple[int, int, int]:
        SAMPLE_SIZE = 10
        VALIDATE_SAMPLE_NUM = 3
        [avatar_height, avatar_width] = avatar_size
        [item_height, item_width] = item_size

        all_item_pixel_xy_list = self._get_pixel_list(item_pixel_list, item_height, item_width)

        if len(all_item_pixel_xy_list) == 0:
            return (0, 0, 0)

        sample_idx = random.sample(range(len(all_item_pixel_xy_list)), min(SAMPLE_SIZE, len(all_item_pixel_xy_list)))
        sample_item_pixel_xy_list = [all_item_pixel_xy_list[i] for i in sorted(sample_idx)]

        data = []
        for pivot_col in range(avatar_width):
            for pivot_row in range(avatar_height):
                ratio = self._get_ratio(
                    pivot_row=pivot_row,
                    pivot_col=pivot_col,
                    avatar_pixel_data=avatar_pixel_list,
                    avatar_height=avatar_height,
                    avatar_width=avatar_width,
                    xy_list=sample_item_pixel_xy_list,
                )
                heappush(data, (ratio, pivot_row, pivot_col))
                if len(data) > VALIDATE_SAMPLE_NUM:
                    heappop(data)

        result = (0, 0, 0)
        for ratio, pivot_row, pivot_col in data:
            correct_ratio = self._get_ratio(
                pivot_row=pivot_row,
                pivot_col=pivot_col,
                avatar_pixel_data=avatar_pixel_list,
                avatar_height=avatar_height,
                avatar_width=avatar_width,
                xy_list=all_item_pixel_xy_list,
            )
            result = max(result, (correct_ratio, pivot_row, pivot_col))
        return result

    def is_contain_by_list(
        self,
        avatar_image: Image.Image,
        item_image: Image.Image,
    ) -> Tuple[int, int, int]:
        """
        image_avatar:
        image_item:
        """
        avatar_pixel_list = list(avatar_image.getdata())
        item_pixel_list = list(item_image.getdata())

        return self.is_contain_by_list(
            avatar_pixel_list=avatar_pixel_list,
            avatar_size=avatar_image.size,
            item_pixel_list=item_pixel_list,
            item_size=item_image.size,
        )

    async def infer_sub(self, image: Image.Image, avatar: Avatar, code: str) -> Tuple[Tuple[int, int, int], int]:
        wcr_response = await self.caller.get_image(avatar=avatar)
        if wcr_response is None:
            return ((0, 0, 0), 0)

        image_data = base64.b64decode(wcr_response)
        item_image = Image.open(io.BytesIO(image_data))
        acc = self.is_contain(avatar_image=image, item_image=item_image), code
        return acc

    async def max_acc_code(self, acc_list: List[Tuple[Tuple[int, int, int], int]]) -> int:
        max_acc = 0
        for acc in acc_list:
            if acc[0][0] >= max_acc:
                max_acc = acc[0][0]
                max_idx_acc = acc[1]
        return max_idx_acc

    async def infer(self, image: Image, item_list: Optional[List[Tuple[int, str]]] = None) -> Avatar:
        # TODO: implement

        avatar = Avatar()

        if item_list is not None:
            acc_lists = [[] for _ in range(4)]
            for idx, code in item_list:
                avatar.add_parts(idx, code)
                acc = await self.infer_sub(image=image, avatar=avatar, code=code)
                acc_lists[idx].append(acc)
                avatar.reset()
            for idx, acc_list in enumerate(acc_lists):
                max_acc = await self.max_acc_code(acc_list)
                avatar.add_parts(idx, max_acc)
            return avatar

        # TODO: 모든코드
