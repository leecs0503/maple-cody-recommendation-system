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
with open('./json_data_result1.json', 'r') as f:
    raw_data: dict = json.load(f)

input_list: List[torch.Tensor] = []
expected_output_list = []
expected_output_tensors = []
cap_set = set()

transform = transforms.Compose([
    transforms.ToTensor(),
    # normalize
])
for crt_name, avatar_info_list in raw_data.items():
    for avatar_info in avatar_info_list:
        weapon_image_b64 = avatar_info["weapon_image"]
        if weapon_image_b64 == "":
            continue
        weapon_image = Image.open(BytesIO(base64.b64decode(weapon_image_b64)))
        weapon_image = weapon_image.convert("RGB")
        weapon_image = weapon_image.resize((224,224), Image.ANTIALIAS)
        input_list.append(transform(weapon_image))
        expected_output_list.append(avatar_info["cap"])
        cap_set.add(avatar_info["cap"])
inv_dict = {}
for idx, val in enumerate(cap_set):
    inv_dict[val] = idx
cap_num = len(cap_set)
expected_output_tensors = []
for output in expected_output_list:
    x = torch.zeros(cap_num)
    x[inv_dict[output]] = 1
    expected_output_tensors.append(x)

# %%
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

epoch_num = 200
learning_rate = 0.002
gamma = 0.1
step_size = 10


model = Model(
    num_result_classes=cap_num,
)
params = model.parameters()

optimizer = optim.Adam(params, lr=learning_rate)
scheduler = lr_scheduler.StepLR(optimizer, step_size=step_size, gamma=gamma)
# criterion = nn.BCELoss(reduction='sum').to(device)
criterion =  nn.CrossEntropyLoss().to(device)

batch_size = 32
for epoch in range(0, epoch_num):
    running_loss = 0.0
    L = [
        (input, answer, eo)
        for input, answer, eo in zip(input_list, expected_output_tensors, expected_output_list)
    ]
    random.shuffle(L)
    run_cnt = 0
    accept_cnt = 0
    all_cnt = 0
    step_num = 0
    for idx in range(0, len(L), batch_size):
        R = L[idx:idx+batch_size]
        inputs = []
        answers = []
        answer_v = []
        for input, answer, eo in R:
            inputs.append(input)
            answers.append(answer)
            answer_v.append(eo)

        input_tensor = torch.stack(inputs)
        answer_tensor = torch.stack(answers)
        output = model(input_tensor)
        loss = criterion(output, answer_tensor)
        optimizer.zero_grad()
        running_loss += loss.item()
        _, o_v = torch.max(output, 1)
        for o, eo in zip(o_v, answer_v):
            eo = inv_dict[eo]
            if o.item() == eo:
                accept_cnt += 1
            all_cnt += 1

        loss.backward()
        optimizer.step()
        run_cnt += 1
        step_num += 1
        print(f"EPOCH [{epoch:3d}] + STEP [{step_num:3d}] loss: {running_loss / run_cnt:.5f} // acc: {accept_cnt / all_cnt:.5f}")
    print(f"EPOCH [{epoch:3d}]: loss: {running_loss / run_cnt:.5f} // acc: {accept_cnt / all_cnt:.5f}")

torch.save(model.state_dict(), './model_result.pth')