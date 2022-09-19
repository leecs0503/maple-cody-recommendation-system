import json


def file_load(json_file_idx: str):
    with open(f"./{json_file_idx}.json") as f:
        json_data = json.load(f)
    return json_data


def json_merge(json_name: list):
    NAME_START_IDX = json_name[0][10:12]  # 10:12 는 입력 된 json_name의 시작 ranking에 해당하는 숫자를 슬라이싱 한 것
    NAME_END_IDX = json_name[-1][13:15]  # 13:15는 입력 된 json_name의 마지막 ranking에 해당하는 숫자를 슬라이싱 한 것

    total_json_data = {
        "info": [],
    }

    for file_idx in range(len(json_name)):
        json_file = file_load(json_name[file_idx])
        for info_idx in range(0, len(json_file["info"])):
            total_json_data["info"].append(json_file["info"][info_idx])

    with open(f"json_data_{NAME_START_IDX}_{NAME_END_IDX}.json", "w") as f:
        json.dump(total_json_data, f, indent=2, ensure_ascii=False)
