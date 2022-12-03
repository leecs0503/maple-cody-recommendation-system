from src.InferenceServer.Model.model import Model
import pytest
import torch


class ModelForTest:
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
def model_for_test() -> Model:
    model = Model(
        name="test",
        model_dir=None,
        model_class_dir="tests.test_inference_server.conftest",
        model_class_name="ModelForTest",
        model_answer_dict_dir="tests/test_inference_server/testdata/model_answer_dict_testdata.json",
    )
    return model