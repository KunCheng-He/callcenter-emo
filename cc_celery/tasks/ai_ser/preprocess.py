import torchaudio
from torch.utils.data import Dataset
from torchaudio import transforms as T

# 音频情感识别的预处理操作

def read_audio_split(file_path: str, frame_length=5, overlap=0.5):
    """
    读取音频文件，并按特定长度进行切分

    参数：
        file_path (str)：音频文件的路径
        frame_length (int, optional)：帧的长度，默认为5秒
        overlap (float, optional)：帧的重叠比例，默认为0.5

    返回：
        segmented_frames (list)：切分后的音频帧列表
        sample_rate (int)：采样率
    """
    # 读取音频文件
    waveform, sample_rate = torchaudio.load(file_path)
    # 计算每一帧的采样点数
    frame_size = int(sample_rate * frame_length)
    # 计算重叠的采样点数
    overlap_size = int(frame_size * overlap)
    # 获取音频文件的总帧数
    total_frames = waveform.size(1)
    # 初始化存储分段的列表
    segmented_frames = []
    # 循环遍历音频文件并分段
    for start in range(0, total_frames, frame_size - overlap_size):
        end = min(start + frame_size, total_frames)
        if end - start == frame_size:  # 确保最后一帧不会超过总帧数
            # 获取当前段的音频数据
            segment = waveform[:, start:end]
            # 将当前段的音频数据添加到列表中
            segmented_frames.append(segment)
    return segmented_frames, sample_rate


class AudioDataset(Dataset):
    """音频数据集类"""
    def __init__(self, segmented_frames):
        """
        初始化函数

        参数:
            segmented_frames (list): 音频帧列表
        """
        self.segmented_frames = segmented_frames
        # MFCC 特征
        self.transform = T.Spectrogram(n_fft=510, hop_length=510 // 2, center=True, pad_mode="reflect", power=2.0)

    def __len__(self):
        return len(self.segmented_frames)

    def __getitem__(self, idx):
        # 获取当前索引对应的音频帧
        waveform = self.segmented_frames[idx]
        # 如果提供了变换函数，则应用变换
        waveform = self.transform(waveform)
        return waveform


if __name__ == '__main__':
    # 测试代码
    file_path = "/home/alchemy/Code/callcenter-emo/upload_files/2024/01/17/test1_left.wav"
    segmented_frames, sample_rate = read_audio_split(file_path)
    dataset = AudioDataset(segmented_frames)
    print(dataset.__getitem__(3))
