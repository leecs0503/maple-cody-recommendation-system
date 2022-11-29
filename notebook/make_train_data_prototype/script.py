# %%
import json
import os
import requests

cwd = os.getcwd()
file_path = os.path.abspath(os.path.join(cwd, os.pardir))
file_path = os.path.abspath(os.path.join(file_path, os.pardir))
file_path = os.path.join(file_path, 'data')

path1 = os.path.join(file_path, 'new_json_data_1_3000.json')
path2 = os.path.join(file_path, 'new_json_data_3001_10000.json')
path3 = os.path.join(file_path, 'new_json_data_10001_15000.json')
path4 = os.path.join(file_path, 'new_json_data_15001_20000.json')
path5 = os.path.join(file_path, 'new_json_data_20001_25000.json')

paths = [path1, path2, path3, path4, path5]
json_datas = []

for path in paths:
    with open(path) as file:
        json_datas.append(json.load(file))


# %%

import requests

cnt = 1
result = {}

for json_data in json_datas:
    for data in json_data['data']:
        result[data["nickname"]] = []
        for code_list in data["recent_cody_list"]:
            encrypted_code = code_list.replace('https://avatar.maplestory.nexon.com/Character/', '').replace('.png', '')
            response = requests.post("http://localhost:8080/character_look_data", json={"packed_character_look": encrypted_code})
            if response.status_code == 200:
                result[data["nickname"]].append(json.loads(response.text))
            else:
                print(response.status_code)
        if len(result) == 100:
            save_path = os.path.join(file_path, f'json_data_result{cnt}.json')
            cnt += 1

            with open(save_path, "w") as f:
                json.dump(result, f, ensure_ascii=False, indent="\t")

            result = {}

if len(result) > 0:
    save_path = os.path.join(file_path, f'json_data_result{cnt}.json')

    cnt += 1

    with open(save_path, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent="\t")

result = {}
save_path = os.path.join(file_path, 'json_data_result_1_25000.json')

for i in range(1, cnt):
    load_path = os.path.join(file_path, f'json_data_result{i}.json')

    with open(load_path, "r") as f:
        temp = json.load(f)
        for k, v in temp.items():
            result[k] = v

with open(save_path, "w") as f:
    json.dump(result, f, ensure_ascii=False, indent="\t")


# %%
