NUM_ITEM = 15


class ItemManager:
    def __init__(self):
        self.data = None

        self.item_codes = [[] for _ in range(NUM_ITEM)]
        self.item_name = dict()
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
            "shoes",
            "faceAccessory",
            "eyeAccessory",
            "earrings",
            "head",
        ]

    def read(self, data: dict):
        self.data = data
        # TODO: 가독성 향상 (메소드 분리)
        for idx, parts in enumerate(self.index_to_parts):
            self.item_codes[idx] = []
            for item_code in self.data[parts]:
                self.item_codes[idx].append(item_code)
                if "name" in self.data[parts][item_code]:
                    self.item_name[item_code] = self.data[parts][item_code]["name"]

    def parts_index_to_str(self, idx: str):
        return self.index_to_parts[idx]

    def get_item_list(self, idx: str):
        assert self.data is not None
        return self.item_codes[idx]

    def get_item_name(self, idx: str):
        if idx in self.item_name:
            return self.item_name[idx]
        return ""
