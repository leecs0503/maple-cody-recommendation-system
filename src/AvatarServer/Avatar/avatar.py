from dataclasses import dataclass
from enum import IntEnum


class AvatarType(IntEnum):
    FACE = 0
    CAP = 1
    LONGCOAT = 2
    WEAPON = 3
    CAPE = 4
    COAT = 5
    GLOVE = 6
    HAIR = 7
    PANTS = 8
    SHIELD = 9
    SHOES = 10
    FACE_ACCESSORY = 11
    EYE_ACCESSORY = 12
    EARRINGS = 13
    SKIN = 14



@dataclass
class Avatar:
    face: str = "0"
    cap: str = "0"
    longcoat: str = "0"
    weapon: str = "0"
    cape: str = "0"
    coat: str = "0"
    glove: str = "0"
    hair: str = "0"
    pants: str = "0"
    shield: str = "0"
    shoes: str = "0"
    faceAccessory: str = "0"
    eyeAccessory: str = "0"
    earrings: str = "0"
    skin: str = "0"

    def add_parts(
        self,
        idx: AvatarType,
        code: str,
    ) -> None:
        # TODO : COAT + PANTS와 LONGCOAT 동시에 불가능하게 로직 추가
        if idx == AvatarType.FACE:
            self.face = code
        elif idx == AvatarType.CAP:
            self.cap = code
        elif idx == AvatarType.LONGCOAT:
            self.longcoat = code
        elif idx == AvatarType.WEAPON:
            self.weapon = code
        elif idx == AvatarType.CAPE:
            self.cape = code
        elif idx == AvatarType.COAT:
            self.coat = code
        elif idx == AvatarType.GLOVE:
            self.glove = code
        elif idx == AvatarType.HAIR:
            self.hair = code
        elif idx == AvatarType.PANTS:
            self.pants = code
        elif idx == AvatarType.SHIELD:
            self.shield = code
        elif idx == AvatarType.SHOES:
            self.shoes = code
        elif idx == AvatarType.FACE_ACCESSORY:
            self.faceAccessory = code
        elif idx == AvatarType.EYE_ACCESSORY:
            self.eyeAccessory = code
        elif idx == AvatarType.EARRINGS:
            self.earrings = code
        elif idx == AvatarType.SKIN:
            self.skin = code
        else:
            raise Exception('Avatar.add_parts : Wrong Type')

    def reset(self):
        self.face = "0"
        self.cap = "0"
        self.longcoat = "0"
        self.weapon = "0"
        self.cape = "0"
        self.coat = "0"
        self.glove = "0"
        self.hair = "0"
        self.pants = "0"
        self.shield = "0"
        self.shoes = "0"
        self.faceAccessory = "0"
        self.eyeAccessory = "0"
        self.earrings = "0"
        self.skin = "0"

    def to_array(self):
        return [
            self.face,
            self.cap,
            self.longcoat,
            self.weapon,
            self.cape,
            self.coat,
            self.glove,
            self.hair,
            self.pants,
            self.shield,
            self.shoes,
            self.faceAccessory,
            self.eyeAccessory,
            self.earrings,
            self.skin
        ]

    def to_param(self):
        return [
            ("face", self.face),
            ("cap", self.cap),
            ("longcoat", self.longcoat),
            ("weapon", self.weapon),
            ("cape", self.cape),
            ("coat", self.coat),
            ("glove", self.glove),
            ("hair", self.hair),
            ("pants", self.pants),
            ("shield", self.shield),
            ("shoes", self.shoes),
            ("faceAccessory", self.faceAccessory),
            ("eyeAccessory", self.eyeAccessory),
            ("earrings", self.earrings),
            ("head", self.skin)
        ]

    @staticmethod
    def single_item_avatar_of(item_num, code):
        avatar = Avatar()
        avatar.add_parts(item_num, code)
        return avatar
