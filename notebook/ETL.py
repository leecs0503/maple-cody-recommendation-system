#%%
import pandas as pd
import json
import random

#%%
random.seed(42)
with open('./data/json_data_result_1_3000.json', 'r') as f:
    raw_data: dict = json.load(f)
    
cnt = 0
info_object = {}
def _add(key, val):
    if key not in info_object:
        info_object[key] = []
    info_object[key].append(val)

for crt_name, avatar_info_list in raw_data.items():
    for avatar_info in avatar_info_list:
        _add('name', crt_name)
        for k, v in avatar_info.items():
            _add(k, v)

raw_df = pd.DataFrame(info_object)
raw_df.head()

df = raw_df.copy()

def extract_hair_base(hair: str):
    if "+" not in hair:
        return hair
    return hair.split('+')[0]

df["hair"] = df["hair"].map(extract_hair_base)
df.head()

from xgboost import XGBClassifier
from sklearn import model_selection
from sklearn.preprocessing import LabelEncoder

train_df, test_df = model_selection.train_test_split(df, test_size=0.05, random_state=42)

def extract_xy(df, idx):
    column_list = train_df.columns.tolist()
    x_col = column_list[1:idx] + column_list[idx + 1:]
    y_col = [column_list[idx]]
    X = train_df[x_col]
    for col_name in X.columns:
        X[col_name] = X[col_name].astype('category')
    y = train_df[y_col]
    return X, y

#%%
def train(want_to_classify_idx: int):
    X, y = extract_xy(train_df, want_to_classify_idx)
    le = LabelEncoder()
    le.fit(y)
    transformed_y = le.transform(y)

    model = XGBClassifier(
        n_estimators=20,
        max_depth=5,
        learning_rate=0.1,
        tree_method="hist",
        objective='multi:softmax',
        enable_categorical=True,
    )
    print(X.head(10))
    xgb_model = model.fit(
        X,
        transformed_y,
        # early_stopping_rounds=100,
        # eval_metric='logloss',
    )
    return xgb_model, le
 
model, le = train(1)

# %%
tx, ty = extract_xy(test_df, 1)
py = model.predict(tx)
print(py)
# %%
