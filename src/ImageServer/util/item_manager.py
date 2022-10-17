import json
from ..Avatar.avatar import Avatar
from ..ImageProcessor.WCR_caller import WCRCaller

NUM_ITEM = 15


class ItemManager:
    def __init__(
        self,
        caller: WCRCaller,
    ) -> None:
        # item manager이 caller이 있는 것ㄷ이 어색함
        self.raw = None
        self.data = None
        self.caller = caller

        self.item_codes = [[] for _ in range(NUM_ITEM)]
        self.item_name = dict()
        self.index_to_raw_parts = [
            "Face",
            "Cap",
            "Longcoat",
            "Weapon",
            "Cape",
            "Coat",
            "Glove",
            "Hair",
            "Pants",
            "Shield",
            "Shoes",
            "Accessory",
            "Accessory",
            "Accessory",
            "Skin",
        ]
        self.index_to_parts = [
            "face",
            "cap",
            "longcoat",
            "weapon",
            "cape",
            "coat",
            "glove",
            "hair",
            "pants",
            "shield",
            "Shoes",
            "faceAccessory",
            "eyeAccessory",
            "earrings",
            "head",
        ]

    def read_raw(self, raw_data: dict):
        self.raw = raw_data

    def read(self, data: dict):
        self.data = data
        for idx, parts in enumerate(self.index_to_parts):
            self.item_codes[idx] = []
            for item_code in self.data[parts]:
                self.item_codes[idx].append(item_code)
                if "name" in self.data[parts][item_code]:
                    self.item_name[item_code] = self.data[parts][item_code]["name"]

    async def validate(self):
        # FIXME: print를 logger로 변경
        # FIXME: refactoring (WCR 수정 후)
        if self.raw is None:
            return
        if self.data is not None:
            return
        if self.caller is None:
            return

        print("Start processing")
        valid_item_num = 0
        self.data = dict()
        for idx, raw_parts in enumerate(self.index_to_raw_parts):
            total_parts_num = 0
            valid_parts_num = 0
            parts = self.index_to_parts[idx]
            self.data[parts] = dict()
            for item_code in self.raw["Eqp"][raw_parts]:
                avatar = Avatar()
                avatar.add_parts(idx, item_code)
                wcr_response = await self.caller.get_image(avatar=avatar)
                total_parts_num += 1
                if wcr_response is None and parts == "weapon":
                    wcr_response = await self.caller.get_image(avatar=avatar, ActionQuery="stand2")
                if wcr_response is not None:
                    valid_parts_num += 1
                    self.data[parts][item_code] = dict()
                    for ckey in self.raw["Eqp"][raw_parts][item_code]:
                        self.data[parts][item_code][ckey] = self.raw["Eqp"][raw_parts][item_code][ckey]
            valid_item_num += valid_parts_num
            print("total_parts_num (", parts, ") :", total_parts_num)
            print("valid_parts_num (", parts, ") :", valid_parts_num)

        print("valid_item_num :", valid_item_num)
        print("Processing Done")
        self.read(self.data)
        with open("valid_wz_code.json", "w") as f:
            json.dump(self.data, f, ensure_ascii=False, indent="\t")

    def parts_index_to_str(self, idx: int):
        return self.index_to_parts[idx]

    def get_item_list(self, idx: int):
        assert self.data is not None
        return self.item_codes[idx]

    def get_item_name(self, idx: int):
        if idx in self.item_name:
            return self.item_name[idx]
        return ""
