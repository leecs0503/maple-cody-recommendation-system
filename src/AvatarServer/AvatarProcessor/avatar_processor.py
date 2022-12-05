import asyncio
import logging
import json
import os
from ..util.item_manager import ItemManager
from ..server.config import Config
from ..Avatar.avatar import Avatar
from .WCR_caller import WCRCaller
from PIL import Image
import base64
import io
from .packed_character_info import PackedCharacterInfo


from Crypto.Cipher import AES
from .structure import STRUCTURE

MS_ABIV = bytes([17, 23, 205, 16, 4, 63, 142, 122, 18, 21, 128, 17, 93, 25, 79, 16])
MS_ABKEY = bytes([16, 4, 63, 17, 23, 205, 18, 21, 93, 142, 122, 25, 128, 17, 79, 20])


class LookStringVersionException(Exception):
    """ 해당 버전에 대한 structure가 존재하지 않는 예외 """


class AvatarProcessor:
    def __init__(
        self,
        logger: logging.Logger,
        config: Config,
        caller: WCRCaller = None,
    ):
        self.logger = logger
        self.base_wz_code_path = config.base_wz_code_path
        self.caller = caller if caller is not None else WCRCaller(
            logger=self.logger,
            wcr_server_host=config.wcr_server_host,
            wcr_server_protocol=config.wcr_server_protocol,
            wcr_server_port=config.wcr_server_port,
            retry_num=config.wcr_caller_retry_num,
            timeout=config.wcr_caller_timeout,
            backoff=config.wcr_caller_backoff,
        )
        self.item_code_list = []
        self.item_manager = ItemManager()
        self.logger.info("start loading base_wz")
        loop = asyncio.get_event_loop()
        base_wz = loop.run_until_complete(
            self._load_base_wz()
        )
        self.item_manager.read(base_wz)
        self.logger.info("complete loading base_wz")

    async def _load_base_wz(self) -> dict:
        if self.base_wz_code_path:
            if os.path.isfile(self.base_wz_code_path):
                base_wz_code_path = self.base_wz_code_path
                with open(base_wz_code_path) as f:
                    base_wz = json.load(f)
                    return base_wz

        base_wz = await self.caller.get_base_wz()

        if self.base_wz_code_path:
            with open(self.base_wz_code_path, "w") as f:
                json.dump(base_wz, f, ensure_ascii=False, indent="\t")
        return base_wz

    async def process_image(self, avatar: Avatar, decode_image: bool = True):
        wcr_response = await self.caller.get_image(avatar=avatar)
        if wcr_response is None:
            return None
        if decode_image:
            image_data = base64.b64decode(wcr_response)
            item_image = Image.open(io.BytesIO(image_data))
            return item_image
        else:
            return wcr_response

    async def get_icon(self, item_code: str):
        return await self.caller.get_icon(item_code=item_code)

    def infer(self, packed_character_look: str) -> PackedCharacterInfo:
        crypt = [
            ((ord(packed_character_look[i]) - ord('A')) << 4)
            + (ord(packed_character_look[i + 1]) - ord('A'))
            for i in range(0, len(packed_character_look), 2)
        ]
        cipher = AES.new(
            key=MS_ABKEY,
            mode=AES.MODE_CBC,
            iv=MS_ABIV,
        )

        data = cipher.decrypt(bytes(crypt))

        version = -1
        offset = 0
        if len(data) == 48:
            version = data[23]
        elif len(data) == 128:
            version = data[119]

        result = PackedCharacterInfo()

        if version not in STRUCTURE:
            raise LookStringVersionException(f"AvatarProcessor.infer: version not exists({version})")

        for now in STRUCTURE[version]:
            value = 0
            for i in range(now.bits):
                if (data[(offset + i) // 8] & (1 << ((offset + i) % 8))) != 0:
                    value |= 1 << i
            offset += now.bits
            if hasattr(result, now.name):
                setattr(result, now.name, value)

        return result
