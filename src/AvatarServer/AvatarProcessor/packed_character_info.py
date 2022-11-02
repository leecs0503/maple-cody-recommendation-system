import dataclasses
from ..Avatar.avatar import Avatar, AvatarType

TYPE_MULTIPLIER = 10000
GENDER_MULTIPLIER = 1000


class CharacterInfoType:
    HEAD = 1
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
    _WEAPONS = [-1, 130, 131, 132, 133, 137, 138, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, -1, 134, 152, 153, -1, 136, 121, 122, 123, 124, 156, 157, 126, 158, 127, 128]  # noqa: E501

    @classmethod
    def get_weapon_type(cls, weapon_id):
        if weapon_id < 0 or weapon_id >= len(cls._WEAPONS):
            return -1
        return cls._WEAPONS[weapon_id]


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
    is_not_blade: int = -1
    is_sub_weapon: int = -1
    shield_id: int = -1
    shield_gender: int = -1
    is_cash_weapon: int = -1
    weapon_id: int = -1
    weapon_gender: int = -1
    weapon_type: int = -1
    hair_mix_color: int = -1
    hair_mix_ratio: int = -1

    def _is_valid_ID(self, item_id: int) -> bool:
        return item_id != -1 and item_id != 1023

    def _is_mix_hair(self) -> bool:
        return (
            0 <= self.hair_mix_color
            and self.hair_mix_color < 8
            and 0 < self.hair_mix_ratio
            and self.hair_mix_ratio < 100
        )

    def _get_ID(self, item_type: int, item_gender: int, item_id: int) -> str:
        return str(item_type * TYPE_MULTIPLIER + item_gender * GENDER_MULTIPLIER + item_id)

    def get_avatar(self) -> Avatar:
        avatar = Avatar()
        if self._is_valid_ID(self.skin_id):
            avatar.add_parts(
                AvatarType.SKIN,
                self._get_ID(
                    item_type=CharacterInfoType.HEAD,
                    item_gender=2,
                    item_id=self.skin_id,
                )
            )
        if self._is_valid_ID(self.face_id):
            avatar.add_parts(
                AvatarType.FACE,
                self._get_ID(
                    item_type=CharacterInfoType.FACE if self.face_type == 0 else CharacterInfoType.FACE2,
                    item_gender=self.face_gender,
                    item_id=self.face_id,
                )
            )
        if self.is_long_coat:
            if not self._is_valid_ID(self.coat_id):
                raise Exception('get_avatar: long coat id required')
            avatar.add_parts(
                AvatarType.LONGCOAT,
                self._get_ID(
                    item_type=CharacterInfoType.LONGCOAT,
                    item_gender=self.coat_gender,
                    item_id=self.coat_id,
                )
            )
        else:
            if self._is_valid_ID(self.coat_id):
                avatar.add_parts(
                    AvatarType.COAT,
                    self._get_ID(
                        item_type=CharacterInfoType.COAT,
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
                avatar.add_parts(
                    AvatarType.PANTS,
                    self._get_ID(
                        item_type=CharacterInfoType.PANTS,
                        item_gender=self.pants_gender,
                        item_id=self.pants_id,
                    )
                )
            else:
                if self.gender == 0:
                    avatar.add_parts(AvatarType.PANTS, "1060026")
                else:
                    avatar.add_parts(AvatarType.PANTS, "1061039")
        if self._is_valid_ID(self.weapon_id) and CharacterInfoType.get_weapon_type(self.weapon_type) != -1:
            if self.is_cash_weapon == 1:
                avatar.add_parts(
                    AvatarType.WEAPON,
                    self._get_ID(
                        item_type=CharacterInfoType.CASHWEAPON,
                        item_gender=self.weapon_gender,
                        item_id=self.weapon_id,
                    )
                )
            else:
                avatar.add_parts(
                    AvatarType.WEAPON,
                    self._get_ID(
                        item_type=CharacterInfoType.get_weapon_type(self.weapon_type),
                        item_gender=self.weapon_gender,
                        item_id=self.weapon_id,
                    )
                )
        if self._is_valid_ID(self.hair_id):
            if self._is_mix_hair():
                avatar.add_parts(
                    AvatarType.HAIR,
                    self._get_ID(
                        item_type=self.hair_type,
                        item_gender=self.hair_gender,
                        item_id=self.hair_id,
                    ) + '+' + str(self.hair_mix_color) + '*' + str(self.hair_mix_ratio)
                )
            else:
                avatar.add_parts(
                    AvatarType.HAIR,
                    self._get_ID(
                        item_type=self.hair_type,
                        item_gender=self.hair_gender,
                        item_id=self.hair_id,
                    )
                )
        if self._is_valid_ID(self.shield_id):
            if not self.is_not_blade:
                avatar.add_parts(
                    AvatarType.SHIELD,
                    self._get_ID(
                        item_type=CharacterInfoType.BLADE,
                        item_gender=self.shield_gender,
                        item_id=self.shield_id,
                    )
                )
            elif self.is_sub_weapon:
                avatar.add_parts(
                    AvatarType.SHIELD,
                    self._get_ID(
                        item_type=CharacterInfoType.SUBWEAPON,
                        item_gender=self.shield_gender,
                        item_id=self.shield_id,
                    )
                )
            else:
                avatar.add_parts(
                    AvatarType.SHIELD,
                    self._get_ID(
                        item_type=CharacterInfoType.SHIELD,
                        item_gender=self.shield_gender,
                        item_id=self.shield_id,
                    )
                )
        item_lists = [
            (self.cap_id, AvatarType.CAP, CharacterInfoType.CAP, self.cap_gender),
            (self.cape_id, AvatarType.CAPE, CharacterInfoType.CAPE, self.cape_gender),
            (self.glove_id, AvatarType.GLOVE, CharacterInfoType.GLOVE, self.glove_gender),
            (self.shoes_id, AvatarType.SHOES, CharacterInfoType.SHOES, self.shoes_gender),
            (self.face_accessory_id, AvatarType.FACE_ACCESSORY, CharacterInfoType.FACE_ACCESSORY, self.face_accessory_gender),
            (self.eye_accessory_id, AvatarType.EYE_ACCESSORY, CharacterInfoType.EYE_ACCESSORY, self.eye_accessory_gender),
            (self.ear_accessory_id, AvatarType.EARRINGS, CharacterInfoType.EAR_ACCESSORY, self.ear_accessory_gender),
        ]
        for item_id, avatar_type, item_type, item_gender in item_lists:
            if self._is_valid_ID(item_id):
                avatar.add_parts(
                    avatar_type,
                    self._get_ID(
                        item_type=item_type,
                        item_gender=item_gender,
                        item_id=item_id
                    )
                )
        return avatar
