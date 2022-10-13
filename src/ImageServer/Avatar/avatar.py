from dataclasses import dataclass


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
    skin: str = "0"

    def add_parts(self, idx, code):
        if idx == 0:
            self.face = code
        elif idx == 1:
            self.cap = code
        elif idx == 2:
            self.longcoat = code
        elif idx == 3:
            self.weapon = code
        elif idx == 4:
            self.cape = code
        elif idx == 5:
            self.coat = code
        elif idx == 6:
            self.glove = code
        elif idx == 7:
            self.hair = code
        elif idx == 8:
            self.pants = code
        elif idx == 9:
            self.shield = code
        elif idx == 10:
            self.shoes = code
        elif idx == 11:
            self.faceAccessory = code
        elif idx == 12:
            self.eyeAccessory = code
        elif idx == 13:
            self.skin = code
        else:
            assert 0

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
            ("head", self.skin)
        ]


# TODO: 안정화 후 사용
# @dataclass
# class Avatar:
#     Accessory: str
#     Cap: str
#     Cape: str
#     Coat: str
#     Face: str
#     Glove: str
#     Hair: str
#     Longcoat: str
#     Pants: str
#     Ring: str
#     Shield: str
#     Shoes: str
#     Weapon: str

#     def to_arr(self):
#         return [
#             self.Accessory,
#             self.Cap,
#             self.Cape,
#             self.Coat,
#             self.Face,
#             self.Glove,
#             self.Hair,
#             self.Longcoat,
#             self.Pants,
#             self.Ring,
#             self.Shield,
#             self.Shoes,
#             self.Weapon,
#         ]
