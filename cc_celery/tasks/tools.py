# 一些基本的处理方法

import re, os
from pydub import AudioSegment

def get_upload_event_info(orig_data: dict):
    """
    获取上传事件信息
    
    Args:
    - orig_data: 原始数据，类型为字典
    
    Returns:
    - event_id: 事件ID
    - cs_user_id: 用户ID
    - file_path: 文件路径
    """
    event_id = orig_data['id']
    cs_user_id = int(re.findall(r'\d+', orig_data['cs_user_id'])[-1])
    file_path = orig_data['file'].split("/upload_files/")[-1]
    return event_id, cs_user_id, file_path


def mp3_separate_left_right(file_path: str):
    """
    分离mp3文件的左右声道
    
    Args:
    - file_path: 原始文件路径
    
    Returns:
    - left_path: 左声道文件路径
    - right_path: 右声道文件路径
    """
    # 另存路径
    left_path = file_path[:-4] + "_left.wav"
    right_path = file_path[:-4] + "_right.wav"
    # 读取音频并分离
    audio = AudioSegment.from_mp3(file_path)
    left = audio.split_to_mono()[0]
    right = audio.split_to_mono()[1]
    # 保存文件
    left.export(left_path, format="wav")
    right.export(right_path, format="wav")
    return left_path, right_path


if __name__ == '__main__':
    # 测试
    filepath = "/home/alchemy/Code/callcenter-emo/upload_files/2024/01/15/test1.mp3"
    left_path, right_path = mp3_separate_left_right(filepath)
    print(left_path, right_path)