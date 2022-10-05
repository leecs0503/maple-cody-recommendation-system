import logging
import random
from ..server.config import Config
from .WCR_caller import WCRCaller


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

    async def is_contain(self, image_avatar, image_item, approach) -> bool:
        SAMPLE_SIZE = 100
        AVATAR_COORD_RATIO = 1
        av_size = image_avatar.size
        item_size = image_item.size
        num_item_pixel = 0

        item_coord = []
        for rows in range(item_size[0]):
            for cols in range(item_size[1]):
                if image_item.getpixel((rows, cols))[3] != 0:
                    num_item_pixel += 1
                    item_coord.append((rows, cols))

        sample_pix_coord = random.sample(item_coord, min(len(item_coord), SAMPLE_SIZE))

        row_coord = list(range(0, av_size[0] - item_size[0] + 1))
        col_coord = list(range(0, av_size[1] - item_size[1] + 1))
        sample_row_coord = random.sample(row_coord, round(len(row_coord) * AVATAR_COORD_RATIO))
        sample_col_coord = random.sample(col_coord, round(len(col_coord) * AVATAR_COORD_RATIO))
        sample_row_coord.sort()
        sample_col_coord.sort()

        print("ㅡㅡㅡㅡ")
        if approach == "sample":
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
                print("accuracy", maximum)
            return maximum

        if approach == "naive":
            SAMPLE_SIZE = 500
            AVATAR_COORD_RATIO = 1

            sample_pix_coord = random.sample(item_coord, min(len(item_coord), SAMPLE_SIZE))

            sample_row_coord = random.sample(row_coord, round(len(row_coord) * AVATAR_COORD_RATIO))
            sample_col_coord = random.sample(col_coord, round(len(col_coord) * AVATAR_COORD_RATIO))
            sample_row_coord.sort()
            sample_col_coord.sort()

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
    async def infer(self, image: Image) -> Avatar:
        # TODO: implement

        avatar = Avatar("1" , "0" , "0" , '0')
        item_image = self.caller.get_image(avatar=avatar)

        if self.is_contain(image, item_image):
            self.item_code_list.append('1')

        result = Avatar(f'{self.item_code_list[0]}' , "0" , "0" , '0')
        return result
"""

"""
        for i in range(30000):
            item_code= i
            avatar = Avatar(f"{i}","0","0",'0') #특정아이템 설정해서 요청

            WCRCaller.get_image(avatar)
            bs64str = web.Request.get.get("bs64")
            item_image_data = base64.b64decode(bs64str)
            item_image = Image.open(io.BytesIO(item_image_data))


            if self.is_contain(image, item_image):
                self.item_code_list.append(f'{i}')

        for i in range(30000):
            item_code= i
            avatar = Avatar("0",f"{i}","0",'0') #특정아이템 설정해서 요청

            WCRCaller.get_image(avatar)
            bs64str = web.Request.get.get("bs64")
            item_image_data = base64.b64decode(bs64str)
            item_image = Image.open(io.BytesIO(item_image_data))


            if self.is_contain(image, item_image):
                self.item_code_list.append(f'{i}')


        for i in range(30000):
            item_code= i
            avatar = Avatar("0","0",f"{i}",'0') #특정아이템 설정해서 요청

            WCRCaller.get_image(avatar)
            bs64str = web.Request.get.get("bs64")
            item_image_data = base64.b64decode(bs64str)
            item_image = Image.open(io.BytesIO(item_image_data))


            if self.is_contain(image, item_image):
                self.item_code_list.append(f'{i}')

        for i in range(30000):
            item_code= i
            avatar = Avatar("0","0","0",f'{i}') #특정아이템 설정해서 요청

            WCRCaller.get_image(avatar)
            bs64str = web.Request.get.get("bs64")
            item_image_data = base64.b64decode(bs64str)
            item_image = Image.open(io.BytesIO(item_image_data))


            if self.is_contain(image, item_image):
                self.item_code_list.append(f'{i}')

        result = Avatar(f'{self.item_code_list[0]}',
        f'{self.item_code_list[1]}',f'{self.item_code_list[2]}',f'{self.item_code_list[3]}')

"""
