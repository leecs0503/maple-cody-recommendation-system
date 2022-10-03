import logging
from PIL import Image

from ..Avatar.avatar import Avatar
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

    async def is_contain(self, image_avatar, image_item) -> bool:
        av_size = image_avatar.size
        item_size = image_item.size
        num_item_pixel = item_size[0] * item_size[1]
        num_item_empty_pixel = 0
        for rows in range(item_size[0]):
            for cols in range(item_size[1]):
                if image_item.getpixel((rows , cols)) == (0 , 0 , 0 , 0):
                    num_item_empty_pixel += 1
        num_item_pixel = num_item_pixel - num_item_empty_pixel

        result = False
        for rows in range(av_size[0] - item_size[0]):
            cnt = 0
            if result:
                break
            for cols in range(av_size[1] - item_size[1]):
                if result:
                    break
                cnt = 0
                for compare_rows in range(item_size[0]):
                    for compare_cols in range(item_size[1]):
                        av_rgba = image_avatar.getpixel((rows + compare_rows, cols + compare_cols))
                        item_rgba = image_item.getpixel((compare_rows, compare_cols))
                        if item_rgba[3] == 0:
                            continue

                        if (av_rgba[0] == item_rgba[0]) and (av_rgba[1] == item_rgba[1]) and (av_rgba[2] == item_rgba[2]):
                            cnt += 1
                else:
                    if num_item_pixel > 440:
                        if num_item_pixel * 0.3 <= cnt:
                            result = True

                    if 400 < num_item_pixel <= 440:
                        if num_item_pixel * 0.4 <= cnt:
                            result = True

                    if 300 < num_item_pixel <= 400:
                        if num_item_pixel * 0.6 <= cnt:
                            result = True

                    if 0 < num_item_pixel <= 300:
                        if num_item_pixel * 0.8 <= cnt:
                            result = True

        return result

    async def infer(self, image: Image) -> Avatar:
        # TODO: implement

        avatar = Avatar("1" , "0" , "0" , '0')
        item_image = self.caller.get_image(avatar=avatar)

        if self.is_contain(image, item_image):
            self.item_code_list.append('1')

        result = Avatar(f'{self.item_code_list[0]}' , "0" , "0" , '0')
        return result


'''
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

'''
