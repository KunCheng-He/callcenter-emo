import os
import torch
from torch.utils.data import DataLoader

from .preprocess import read_audio_split, AudioDataset
from .models import LightSERNet

# 音频情感识别

def recognize_sentiment(audio_file_path: str, model_path: str):
    """
    识别音频文件的情感

    参数：
        audio_file_path (str): 音频文件的路径
        model_path (str): 模型路径

    返回：
        emotion_result (list): 情感识别结果列表
    """
    # 构建数据集
    segmented_frames, sample_rate = read_audio_split(audio_file_path)
    dataset = AudioDataset(segmented_frames, sample_rate)
    data_loader = DataLoader(dataset, batch_size=1, shuffle=False)
    # 加载识别模型
    # net_pth = os.path.join(os.getcwd(), "cc_celery/tasks/ai_ser/models_pth/LightSERNet.pth")
    net = LightSERNet()
    net.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    # 识别结果
    emotion_result = []
    # 识别
    net.eval()
    for data in data_loader:
        y = net(data)
        emotion_result.append(torch.argmax(y, dim=1).item())
    return emotion_result
