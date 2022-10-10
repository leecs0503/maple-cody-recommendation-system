

class ItemManager:
    def __init__(self) -> None:
        self.raw = None
        self.index_to_parts = []
        self.item_codes = [[] for _ in range(14)]
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

    def get_item_list(self, idx: int):
        assert self.raw is not None
        return self.item_codes[idx]
