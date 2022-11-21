from torchvision.models import resnet18
from torch import nn
import torch

class Model(nn.Module):
    def __init__(
        self,
        num_result_classes,
    ):
        super().__init__()
        image_model = resnet18(pretrained=False)
        num_ftrs = image_model.fc.in_features # 1000
        image_model.fc = nn.Linear(num_ftrs, num_ftrs) 
        self.image_model = image_model
        self.fc1 = nn.Linear(num_ftrs, num_result_classes)
        self.fc2 = nn.Linear(num_result_classes, num_result_classes)
        self.dropout = nn.Dropout(0.5)
        self.sigmoid = torch.nn.Sigmoid()

    def forward(
        self,
        image_tensor,
    ):
        result_feature = self.image_model(image_tensor)
        
        l2_norm = result_feature.norm(p=2, dim=1, keepdim=True).detach()
        result_feature = result_feature.div(l2_norm) # l2-normalized feature vector
        result_feature = self.sigmoid(result_feature)
        result_feature = self.dropout(result_feature)
        result_feature = self.fc1(result_feature)
        result_feature = self.sigmoid(result_feature)
        result_feature = self.dropout(result_feature)
        result_feature = self.fc2(result_feature)
        return result_feature
