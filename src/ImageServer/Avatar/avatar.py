from dataclasses import dataclass


@dataclass
class Avatar:
    face: str
    hair: str
    longcoat: str
    weapon: str

    def to_array(self):
        return [
            self.face,
            self.hair,
            self.longcoat,
            self.weapon,
        ]

    def to_param(self):
        return [
            ("Face", self.face),
            ("Hair", self.hair),
            ("Longcoat", self.longcoat),
            ("Weapon", self.weapon),
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