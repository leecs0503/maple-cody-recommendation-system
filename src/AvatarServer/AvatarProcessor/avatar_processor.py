import asyncio
import logging
import json
import os
from ..util.item_manager import ItemManager
from ..server.config import Config
from ..Avatar.avatar import Avatar, AvatarType
from .WCR_caller import WCRCaller
from PIL import Image
import base64
import io
import dataclasses

from Crypto.Cipher import AES
from .structure import STRUCTURE

MS_ABIV = bytes([17, 23, 205, 16, 4, 63, 142, 122, 18, 21, 128, 17, 93, 25, 79, 16])
MS_ABKEY = bytes([16, 4, 63, 17, 23, 205, 18, 21, 93, 142, 122, 25, 128, 17, 79, 20])

TYPE_MULTIPLIER = 10000
GENDER_MULTIPLIER = 1000

FACE = 2
HAIR = 3
HAIR2 = 4
FACE2 = 5
HAIR3 = 6
CAP = 100
FACE_ACCESSORY = 101
EYE_ACCESSORY = 102
EAR_ACCESSORY = 103
COAT = 104
LONGCOAT = 105
PANTS = 106
SHOES = 107
GLOVE = 108
CAPE = 110
SHIELD = 109
BLADE = 134
SUBWEAPON = 135
CASHWEAPON = 170
WEAPONS = [-1, 130, 131, 132, 133, 137, 138, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, -1, 134, 152, 153, -1, 136, 121, 122, 123, 124, 156, 157, 126, 158, 127, 128]


@dataclasses.dataclass
class PackedCharacterInfo:
    gender: int = -1
    skin_id: int = -1
    face_type: int = -1
    face_id: int = -1
    face_gender: int = -1
    hair_type: int = -1
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

    def _is_valid_ID(item_id: int) -> bool:
        return item_id != -1 and item_id != 1023

    def _get_ID(self, item_type: int, item_gender: int, item_id: int) -> str:
        return str(item_type * TYPE_MULTIPLIER + item_gender * GENDER_MULTIPLIER + item_id)

    def get_avatar(self) -> Avatar:
        avatar = Avatar()
        if self._is_valid_ID(self.face_id):
            avatar.add_parts(
                AvatarType.FACE,
                self._get_ID(
                    item_type=FACE if self.face_type == 0 else FACE2,
                    item_gender=self.face_gender,
                    item_id=self.face_id,
                )
            )
        if self._is_valid_ID(self.cap_id):
            avatar.add_parts(
                AvatarType.CAP,
                self._get_ID(
                    item_type=CAP,
                    item_gender=self.cap_gender,
                    item_id=self.cap_id,
                )
            )
        if self.is_long_coat:
            if not self._is_valid_ID(self.coat_id):
                raise Exception('get_avatar: long coat id required')
            avatar.add_parts(
                AvatarType.LONGCOAT,
                self._get_ID(
                    item_type=LONGCOAT,
                    item_gender=self.coat_gender,
                    item_id=self.coat_id,
                )
            )
        else:
            if self._is_valid_ID(self.coat_id):
                avatar.add_parts(
                    AvatarType.COAT,
                    self._get_ID(
                        item_type=COAT,
                        item_gender=self.coat_gender,
                        item_id=self.coat_id,
                    )
                )
            else:
                if self.gender == 0:
                    avatar.add_parts(AvatarType.COAT, "1040036")
                else:
                    avatar.add_parts(AvatarType.COAT, "1041046")
            if self._is_valid_ID(self.pants_id):
                pass
        return avatar


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

        for now in STRUCTURE[version]:
            value = 0
            for i in range(now.bits):
                if (data[(offset + i) // 8] & (1 << ((offset + i) % 8))) != 0:
                    value |= 1 << i
            offset += now.bits
            if hasattr(result, now.name):
                setattr(result, now.name, value)

        return result
