#%%
import json
import os
import pandas

base_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(base_path, 'data', 'json_data_result_1_3000.json')

with open(data_path, 'r') as f:
    data = json.load(f)

formatted_data = {}

for name, v in data.items():
    for obj in v:
        if "name" not in formatted_data:
            formatted_data["name"] = []
        formatted_data["name"].append(name)
        for item_type, item_code in obj.items():
            if item_type not in formatted_data:
                formatted_data[item_type] = []
            formatted_data[item_type].append(item_code)
    
# %%
df = pandas.DataFrame(formatted_data)
df.head(10)

# %%
import xgboost
xgboost.XGB

