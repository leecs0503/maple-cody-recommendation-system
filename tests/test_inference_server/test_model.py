from src.InferenceServer.Model.complement_model import KserveComplementModel
import json
import os


def test_request(model_for_test: KserveComplementModel):
    cwd = os.path.dirname(__file__)
    json_path = os.path.join(cwd, "testdata", "predict_input.json")
    with open(json_path) as f:
        data = json.load(f)
    json_path = os.path.join(cwd, "testdata", "female_face_answer_dict.json")
    with open(json_path) as f:
        expected_result = json.load(f)
    result = model_for_test.predict(request={"instances": data})

    result = result["predictions"]

    for image_num in range(len(data)):
        for class_num, (probability, result_item_code) in enumerate(result[image_num]):
            for index, expected_item_code in expected_result.items():
                if expected_item_code == result_item_code:
                    assert index == f"{probability}"
