import kserve
from typing import Dict
from PIL import Image
from io import BytesIO
import torch
import importlib
import base64
import torchvision.transforms as transforms


class Model(kserve.Model):
    def __init__(
        self,
        name: str,
        model_dir: str,
        model_class_dir: str,
        model_class_name: str,
    ):
        super().__init__(name)
        self.name = name
        self.model_dir = model_dir
        self.model_class_dir = model_class_dir
        self.model_class_name = model_class_name
        self.ready = False
        self.model = None
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            # normalize
        ])

    def load(self) -> bool:
        # Load the python class into memory
        model_class = getattr(importlib.import_module(self.model_class_dir), self.model_class_name)

        self.model = model_class().to(self.device)
        self.model.load_state_dict(torch.load(self.model_dir, map_location=self.device))
        self.model.eval()
        self.ready = True
        return self.ready

    def predict(self, request: Dict) -> Dict:
        with torch.no_grad():
            try:
                raw_inputs = request["instances"]
                inputs = []
                for raw_input in raw_inputs:
                    input_image = Image.open(BytesIO(base64.b64decode(raw_input)))
                    input_image = input_image.convert("RGB")
                    input = input_image.resize((224, 224), Image.ANTIALIAS)
                    inputs.append(self.transform(input))
                inputs = torch.tensor(inputs).to(self.device)
            except Exception as e:
                raise TypeError(
                    "Failed to initialize Torch Tensor from inputs: %s, %s" % (e, inputs))
            try:
                outputs = self.model(inputs)
                _, output_index = torch.max(outputs, 1)
                # TODO: output index를 실제 코드로 변환하는 로직 추가
                return {"predictions": output_index.tolist()}
            except Exception as e:
                raise Exception("Failed to predict %s" % e)
