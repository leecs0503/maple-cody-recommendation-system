# %%
import json
import os
import requests

cwd = os.getcwd()
file_path = os.path.abspath(os.path.join(cwd, os.pardir))
file_path = os.path.abspath(os.path.join(file_path, os.pardir))
file_path = os.path.join(file_path, 'data')

path1 = os.path.join(file_path, 'json_data_1_1000.json')
path2 = os.path.join(file_path, 'json_data_1001_2000.json')
path3 = os.path.join(file_path, 'json_data_2001_3000.json')

with open(path1) as file:
    json_data1 = json.load(file)

with open(path2) as file:
    json_data2 = json.load(file)

with open(path3) as file:
    json_data3 = json.load(file)

# %%
result = {}

for json_data in [json_data1, json_data2, json_data3]:
    for data in json_data['data']:
        result[data["nickname"]] = []
        for code_list in data["recent_cody_list"]:
            encrypted_code = code_list.replace('https://avatar.maplestory.nexon.com/Character/', '').replace('.png', '')
            response = requests.post("http://localhost:8080/packed_character_look", json={"packed_character_look": encrypted_code})  # noqa: E501
            if response.status_code == 200:
                result[data["nickname"]].append(json.loads(response.text))

save_path = os.path.join(file_path, 'json_data_result_1_3000.json')

with open(save_path, "w") as f:
    json.dump(result, f, ensure_ascii=False, indent="\t")
# %%
