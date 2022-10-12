
NUM_ITEM = 14


class ItemManager:
    def __init__(self) -> None:
        self.raw = None
        self.index_to_parts = []
        self.item_codes = [[] for _ in range(14)]
        self.item_name = dict()
        self.index_to_parts.append("Face")
        self.index_to_parts.append("Cap")
        self.index_to_parts.append("Longcoat")
        self.index_to_parts.append("Weapon")
        self.index_to_parts.append("Cape")
        self.index_to_parts.append("Coat")
        self.index_to_parts.append("Glove")
        self.index_to_parts.append("Hair")
        self.index_to_parts.append("Pants")
        self.index_to_parts.append("Shield")
        self.index_to_parts.append("Shoes")
        self.index_to_parts.append("Accessory")
        self.index_to_parts.append("Accessory")
        self.index_to_parts.append("Skin")

    def read(self, raw_data: dict):
        self.raw = raw_data
        for idx, parts in enumerate(self.index_to_parts):
            self.item_codes[idx] = []
            for item_code in self.raw["Eqp"][parts].keys():
                self.item_codes[idx].append(item_code)
                if "name" in self.raw["Eqp"][parts][item_code]:
                    self.item_name[item_code] = self.raw["Eqp"][parts][item_code]["name"]
                else:
                    print(item_code)

    def parts_index_to_str(self, idx: int):
        return self.index_to_parts[idx]

    def get_item_list(self, idx: int):
        assert self.raw is not None
        return self.item_codes[idx]

    def get_item_name(self, idx: int):
        if idx in self.item_name:
            return self.item_name[idx]
        return ""
