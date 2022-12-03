from src.InferenceServer.Model.complement_model import KserveComplementModel
import pytest
import torch


class ComplementModelForTest:
    def __init__(self, num_classes: int):
        self.num_classes = num_classes

    def to(self, _):
        return self

    def __call__(self, input_tensor):
        result = []
        for _ in range(input_tensor.shape[0]):
            result.append(torch.tensor(
                list(range(self.num_classes))
            ))
        return torch.stack(result)


@pytest.fixture
def model_for_test() -> KserveComplementModel:
    model = KserveComplementModel(
        name="test",
        model_dir="",
        model_answer_dict_dir="tests/test_inference_server/testdata/model_answer_dict_testdata.json",
    )
    model.model = ComplementModelForTest(model.num_classes)
    return model
