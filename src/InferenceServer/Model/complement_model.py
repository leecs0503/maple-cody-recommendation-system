import kserve
from typing import Dict
from PIL import Image
from io import BytesIO
from src.Trainer.models.complement_model.model import ComplementModel
import torch
import base64
import torchvision.transforms as transforms
import json


class KserveComplementModel(kserve.Model):
    def __init__(
        self,
        name: str,
        model_dir: str,
        model_answer_dict_dir: str,
    ):
        super().__init__(name)
        self.name = name
        self.model_dir = model_dir
        self.ready = False
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            # normalize
        ])
        try:
            with open(model_answer_dict_dir, "r") as f:
                self.answer_dict = json.load(f)
        except Exception as err:
            raise Exception(f"model answer not found({str(err)})")

        self.num_classes = len(self.answer_dict)

        self.model = ComplementModel(self.num_classes).to(self.device)

    def load(self) -> bool:
        self.model.load_state_dict(torch.load(self.model_dir, map_location=self.device))
        self.model.eval()
        self.ready = True
        return self.ready

    def predict(self, request: Dict) -> Dict:
        inputs = []
        with torch.no_grad():
            try:
                raw_inputs = request["instances"]
                for raw_input in raw_inputs:
                    input_image = Image.open(BytesIO(base64.b64decode(raw_input)))
                    input_image = input_image.convert("RGB")
                    input = input_image.resize((224, 224), Image.ANTIALIAS)
                    inputs.append(self.transform(input))
                inputs = torch.stack(inputs).to(self.device)
            except Exception as e:
                raise TypeError(
                    "Failed to initialize Torch Tensor from inputs: %s, %s" % (e, inputs))
            try:
                outputs = self.model(inputs)
                result = []
                for image_num in range(inputs.shape[0]):
                    index_list = [
                        (outputs[image_num, class_num].item(), self.answer_dict[f"{class_num}"])
                        for class_num in range(self.num_classes)
                    ]
                    index_list.sort(reverse=True)
                    result.append(index_list[:5])

                return {"predictions": result}
            except Exception as e:
                raise Exception("Failed to predict %s" % e)
