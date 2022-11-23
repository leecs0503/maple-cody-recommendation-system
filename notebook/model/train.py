# %%
from model import Model
import json
import random

import torch.optim as optim
from torch.optim import lr_scheduler
import torch
from torch import nn

# %%
from PIL import Image
import base64
from io import BytesIO
import torchvision.transforms as transforms
from typing import List
random.seed(42)
device = torch.device("cuda")
with open('./json_data_result_1_3000.json', 'r') as f:
    raw_data: dict = json.load(f)

input_list: List[torch.Tensor] = []
weapon_set = set()
expected_output_list = []
expected_output_tensors = []
cap_set = set()
datas = {}
def add_datas(K, V):
    if K not in datas:
        datas[K] = []
    datas[K].append(V)

transform = transforms.Compose([
    transforms.ToTensor(),
    # normalize
])
for crt_name, avatar_info_list in raw_data.items():
    for avatar_info in avatar_info_list:
        weapon_image_b64 = avatar_info["weapon_image"]
        add_datas(avatar_info["weapon"], avatar_info["cap"])
        if weapon_image_b64 == "":
            continue

        weapon_set.add(
            (avatar_info["weapon"], weapon_image_b64)
        )
        cap_set.add(avatar_info["cap"])
inv_dict = {}
for idx, val in enumerate(cap_set):
    inv_dict[val] = idx
cap_num = len(cap_set)
expected_output_tensors = []

for (weapon, weapon_image_b64) in weapon_set:
    weapon_image = Image.open(BytesIO(base64.b64decode(weapon_image_b64)))
    weapon_image = weapon_image.convert("RGB")
    result = weapon_image.resize((224, 224), Image.ANTIALIAS)
    # result = Image.new(weapon_image.mode, (224, 224), (0, 0, 0))
    # result.paste(weapon_image, (0, 0))
    # result.show()
    L = datas[weapon]
    output = torch.zeros(cap_num)
    for cap in L:
        output[inv_dict[cap]] += 1
    output = output.div(torch.sum(output))
    input_list.append(transform(result))
    expected_output_tensors.append(output)
print(len(input_list))
# for output in expected_output_list:
#     # x = torch.zeros(cap_num, dtype=torch.long).to(device)
#     # x[inv_dict[output]] = 1
#     expected_output_tensors.append(torch.tensor([inv_dict[output]]))

# %%

epoch_num = 1000
learning_rate = 0.001
gamma = 0.1
step_size = 20


model = Model(
    num_result_classes=cap_num,
).to(device)
params = model.parameters()

optimizer = optim.Adam(params, lr=learning_rate)
# scheduler = lr_scheduler.ReduceLROnPlateau(optimizer, 'min')
scheduler = lr_scheduler.StepLR(optimizer, step_size=step_size, gamma=gamma)
# criterion = nn.BCELoss(reduction="sum").to(device)
criterion =  nn.MSELoss(reduction="sum").to(device)

batch_size = 32
for epoch in range(0, epoch_num):
    running_loss = 0.0
    L = [
        (input, answer)
        for input, answer in zip(input_list, expected_output_tensors)
    ]
    random.shuffle(L)
    run_cnt = 0
    accept_cnt = 0
    all_cnt = 0
    step_num = 0
    for idx in range(0, len(L), batch_size):
        R = L[idx:idx+batch_size]
        bs = len(R)
        inputs = []
        answers = []
        for input, answer in R:
            inputs.append(input)
            answers.append(answer)

        input_tensor = torch.stack(inputs).to(device)
        answer_tensor = torch.stack(answers).to(device)
        output = model(input_tensor)
        loss = criterion(output, answer_tensor)
        optimizer.zero_grad()
        running_loss += loss.item()
        _, o_v = torch.max(output, 1)
        qqq = 0
        for o, answer_tensor in zip(o_v, answers):
            if not -1e-9 <= answer_tensor[o.item()] <= 1e-9:
                accept_cnt += 1
            all_cnt += 1

        loss.backward()
        optimizer.step()
        run_cnt += 1
        step_num += 1
        # if step_num % 10 == 0:
        #     print(f"EPOCH [{epoch:3d}] + STEP [{step_num:3d}] loss: {running_loss / run_cnt:.5f} // acc: {accept_cnt / all_cnt:.5f}")
    print(f"EPOCH [{epoch:3d}]: loss: {running_loss / all_cnt:.5f} // acc: {accept_cnt / all_cnt:.5f}")
    scheduler.step()

torch.save(model.state_dict(), './model_result.pth')