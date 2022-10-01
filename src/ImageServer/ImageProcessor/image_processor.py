import logging
import io
from PIL import Image

from ..Avatar.avatar import Avatar
from ..server.config import Config
from .WCR_caller import WCRCaller
import base64


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
        '''
        pix_avatar = np.array(image_avatar)
        pix_item = np.array(image_item)

        size_avatar = np.array(image_avatar.size)
        size_item = np.array(image_item.size)

        start_point = []
        for rows in range(size_avatar[0]):
            for columns in range(size_item[1]):
                if pix_avatar[rows][columns][3] == 255:
                    if size_item[0] + rows < size_avatar[0]:
                        if size_item[1] + columns < size_avatar[1]:
                            start_point.append((rows,columns))

        for idx in range(len(start_point)):
            cnt=0
            for rows in range(start_point[idx][0], start_point[idx][0] + size_item[0] + 1):
                for col in range(start_point[idx][1], start_point[idx][1] + size_item[1] + 1):
                    if pix_avatar == pix_item:
                        cnt+=1
            if cnt == size_item[0] * size_item[1]:
                return True
        '''
        return True

    async def infer(self, image: Image) -> Avatar:
        # TODO: implement

        avatar = Avatar("1" , "0" , "0" , '0')
        a = WCRCaller()
        response = await a.get_image(avatar=avatar)
        bs64str = response.get("bs64")

        item_image_data = base64.b64decode(bs64str)
        item_image = Image.open(io.BytesIO(item_image_data))

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
