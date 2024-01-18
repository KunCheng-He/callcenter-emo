import torch
from torch import nn
from typing import Union

# 语音情感识别所用的AI模型

class LightSERBlook(nn.Module):
    """ Light-SERNet 的一个卷积模块 """
    def __init__(self, in_channel: int, out_channel: int, kernel_size: Union[int, tuple], padding: Union[int, tuple], \
                 stride: Union[int, tuple], pool_size: Union[int, tuple], pool_pad: Union[int, tuple], \
                    pool_stride: Union[int, tuple], bias=True) -> None:
        """
        参数:
            in_channel: 输入通道
            out_channel: 输出通道
            kernel_size: 卷积核大小
            padding: 填充
            stride: 步长
            pool_size: 池化大小
            pool_pad: 池化填充
            pool_stride: 池化步长
            bias: 卷积是否使用偏置，默认为 True
        """
        super().__init__()
        self.conv = nn.Conv2d(
            in_channels=in_channel, out_channels=out_channel,
            kernel_size=kernel_size, padding=padding, stride=stride, bias=bias
        )
        self.bn = nn.BatchNorm2d(out_channel)
        self.relu = nn.ReLU()
        self.avgpool = nn.AvgPool2d(kernel_size=pool_size, padding=pool_pad, stride=pool_stride)

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        x = self.avgpool(x)
        return x


class LightSERNet(nn.Module):
    """ Light-SERNet 完整的模型 """
    def __init__(self) -> None:
        super().__init__()

        # Body Part I : Parallel Paths
        self.part1_1 = LightSERBlook(1, 32, 3, 1, 1, 2, 0, 2)             # 卷积通过 pad 并没有改变输入的大小
        self.part1_2 = LightSERBlook(1, 32, (11, 1), (5, 0), 1, 2, 0, 2)  # avgpool 步长为 2，所以输出形状折半
        self.part1_3 = LightSERBlook(1, 32, (1, 9), (0, 4), 1, 2, 0, 2)

        # Body Part II : Feature Learning (LFLBs)
        self.part2_1 = LightSERBlook(32, 64, 3, 1, 1, 2, 0, 2, bias=False)  # 卷积不变，池化减半
        self.part2_2 = LightSERBlook(64, 96, 3, 1, 1, 2, 0, 2, bias=False)
        self.part2_3 = LightSERBlook(96, 128, 3, 1, 1, (2, 1), 0, (2, 1), bias=False)  # 卷积不变，池化纵向减半，横向不变
        self.part2_4 = LightSERBlook(128, 160, 3, 1, 1, (2, 1), 0, (2, 1), bias=False)
        self.part2_5 = nn.Sequential(
            nn.Conv2d(160, 320, 1, 1, 0, bias=False),  # 卷积不变
            nn.BatchNorm2d(320),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1)  # 对每个通道的全部 H*W 进行平均，最后保留的是 (batch_size, Channel, 1, 1)
        )

        # Head : Classifier
        self.dropout = nn.Dropout(0.2)
        self.line = nn.Linear(320, 3)
        self.endActivate = nn.Softmax(dim=1)

    def forward(self, x):  # x.shape: torch.Size([b, 1, 157, 50])
        x1_1 = self.part1_1(x)  # x1_*.shape: torch.Size([b, 32, 78, 25])
        x1_2 = self.part1_2(x)
        x1_3 = self.part1_3(x)
        x = torch.cat([x1_1, x1_2, x1_3], dim=-1)  # torch.Size([b, 32, 78, 75])
        x = self.part2_1(x)  # torch.Size([b, 64, 39, 37])
        x = self.part2_2(x)  # torch.Size([b, 96, 19, 18])
        x = self.part2_3(x)  # torch.Size([b, 128, 9, 18])
        x = self.part2_4(x)  # torch.Size([b, 160, 4, 18])
        x = self.part2_5(x)  # torch.Size([b, 320, 1, 1])
        x = x.squeeze(dim=(-1, -2))  # torch.Size([b, 320])
        x = self.dropout(x)
        x = self.line(x)  # torch.Size([b, 3])
        x = self.endActivate(x)
        return x


if __name__ == '__main__':
    # 测试模型
    net_pth = "/home/alchemy/Code/callcenter-emo/cc_celery/tasks/ai_ser/models_pth/LightSERNet.pth"
    model = LightSERNet()
    model.load_state_dict(torch.load(net_pth, map_location=torch.device('cpu')))
    x = torch.randn(1, 1, 157, 50)
    y = model(x)
    print(y.shape)
