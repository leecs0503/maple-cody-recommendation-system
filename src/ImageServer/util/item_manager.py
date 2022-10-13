import json
from ..Avatar.avatar import Avatar
from ..ImageProcessor.WCR_caller import WCRCaller


NUM_ITEM = 15


class ItemManager:
    def __init__(self) -> None:
        self.raw = None
        self.data = None
        self.caller = None
        self.index_to_raw_parts = []
        self.index_to_parts = []
        self.item_codes = [[] for _ in range(NUM_ITEM)]
        self.item_name = dict()
        self.index_to_raw_parts.append("Face")
        self.index_to_raw_parts.append("Cap")
        self.index_to_raw_parts.append("Longcoat")
        self.index_to_raw_parts.append("Weapon")
        self.index_to_raw_parts.append("Cape")
        self.index_to_raw_parts.append("Coat")
        self.index_to_raw_parts.append("Glove")
        self.index_to_raw_parts.append("Hair")
        self.index_to_raw_parts.append("Pants")
        self.index_to_raw_parts.append("Shield")
        self.index_to_raw_parts.append("Shoes")
        self.index_to_raw_parts.append("Accessory")
        self.index_to_raw_parts.append("Accessory")
        self.index_to_raw_parts.append("Accessory")
        self.index_to_raw_parts.append("Skin")

        self.index_to_parts.append("face")
        self.index_to_parts.append("cap")
        self.index_to_parts.append("longcoat")
        self.index_to_parts.append("weapon")
        self.index_to_parts.append("cape")
        self.index_to_parts.append("coat")
        self.index_to_parts.append("glove")
        self.index_to_parts.append("hair")
        self.index_to_parts.append("pants")
        self.index_to_parts.append("shield")
        self.index_to_parts.append("Shoes")
        self.index_to_parts.append("faceAccessory")
        self.index_to_parts.append("eyeAccessory")
        self.index_to_parts.append("earrings")
        self.index_to_parts.append("head")

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
        if self.raw is None or self.data is not None or self.caller is not None:
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
