from typing import Dict
from typing import List
from PIL import Image
from io import BytesIO
import base64
import torch
import torchvision.transforms as transforms

class RawData:
    def __init__(
        self,
        raw_data: Dict,
        transform: transforms.Compose,
    ) -> None:
        weapon_set = set()
        input_list: List[torch.Tensor] = []
        output_list: List[int] = []

        for crt_name, avatar_info_list in raw_data.items():
            for avatar_info in avatar_info_list:
                weapon = avatar_info["weapon"]
                weapon_image_b64 = avatar_info["weapon_image"]
                if weapon_image_b64 == "":
                    continue
                weapon_set.add(weapon)
                weapon_image = Image.open(BytesIO(base64.b64decode(weapon_image_b64)))
                weapon_image = weapon_image.convert("RGB")
                result = weapon_image.resize((224, 224), Image.ANTIALIAS)
                input_list.append(transform(result))
                output_list.append(weapon)

        inv_dict = {}
        for idx, val in enumerate(weapon_set):
            inv_dict[val] = idx
        output_list = [
            inv_dict[output]
            for output in output_list
        ]

        self.input_list = input_list
        self.output_list = output_list
