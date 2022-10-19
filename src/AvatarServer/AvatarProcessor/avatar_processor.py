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
import dataclasses


@dataclasses.dataclass
class PackedCharacterInfo:
    gender: int = -1
    skin_id: int = -1
    face_id: int = -1
    face_gender: int = -1
    is_hair_over_40000: int = -1
    hair_id: int = -1
    hair_gender: int = -1
    cap_id: int = -1
    cap_gender: int = -1
    face_accessory_id: int = -1
    face_accessory_gender: int = -1
    eye_accessory_id: int = -1
    eye_accessory_gender: int = -1
    ear_accessory_id: int = -1
    ear_accessory_gender: int = -1
    is_long_coat: int = -1
    coat_id: int = -1
    coat_gender: int = -1
    pants_id: int = -1
    pants_gender: int = -1
    shoes_id: int = -1
    shoes_gender: int = -1
    glove_id: int = -1
    glove_gender: int = -1
    cape_id: int = -1
    cape_gender: int = -1
    shield_id: int = -1
    shield_gender: int = -1
    weapon_id: int = -1
    weapon_gender: int = -1
    hair_mix_color: int = -1
    hair_mix_ratio: int = -1


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
        self.item_manager = ItemManager(
            caller=self.caller
        )
        loop = asyncio.get_event_loop()
        base_wz = loop.run_until_complete(
            self._load_base_wz()
        )
        self.item_manager.read_raw(base_wz)
        loop.run_until_complete(
            self.item_manager.validate()
        )

    async def _load_base_wz(self) -> dict:
        # TODO: 위치 논의 필요
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

    async def process_image(self, avatar: Avatar):
        wcr_response = await self.caller.get_image(avatar=avatar)
        if wcr_response is None:
            return None

        image_data = base64.b64decode(wcr_response)
        item_image = Image.open(io.BytesIO(image_data))
        return item_image

    def infer(self, packed_character_look: str) -> Avatar:
        # TODO: implement
        return PackedCharacterInfo()