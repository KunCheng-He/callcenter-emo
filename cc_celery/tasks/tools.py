# 一些基本的处理方法

import re, os, zipfile
from pydub import AudioSegment

from apps.audio.models import Audio
from apps.upload_events.models import UploadEvent

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
    event_id = int(re.findall(r'\d+', orig_data['url'])[-1])
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


def get_relative_path(file_path: str, base_path: str):
    """
    获取相对路径

    Args:
    - file_path: 原始文件路径
    - base_path: 基础路径
    Returns:
    - relative_path: 相对路径
    """
    relative_path = os.path.normpath(file_path.replace(base_path, '', 1))
    return relative_path


def unzip_file(file_path: str):
    """
    解压缩文件

    Args:
        file_path (str): 压缩文件的路径

    Returns:
        str: 解压后的文件路径
    """
    unzip_path = file_path[:-4] + "_unzip"
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(unzip_path)
    return unzip_path


def mp3_add_database(event_id: int, file_path: str):
    """
    将mp3格式的文件转换为wav格式的文件，并将其加入音频数据表

    Args:
        event_id (int): 上传事件实例的ID
        file_path (str): mp3格式文件的路径
        
    Returns:
        audio_id (int): 音频实例的ID
    """
    # 处理mp3格式的文件为wav格式的文件
    left_path, right_path = mp3_separate_left_right(file_path)
    # 获取上传事件实例
    upload_object = UploadEvent.objects.get(id=event_id)
    # 将分离出的音频加入音频数据表
    audio_object = Audio.objects.create(
        orig_file_path = get_relative_path(file_path, os.getcwd()),
        left_file_path = get_relative_path(left_path, os.getcwd()),
        right_file_path = get_relative_path(right_path, os.getcwd()),
        upload_event_id = upload_object
    )
    audio_object.save()
    audio_id = audio_object.id
    return audio_id


if __name__ == '__main__':
    # 测试
    filepath = "/home/alchemy/Code/callcenter-emo/upload_files/2024/01/15/test.zip"
    print(unzip_file(filepath))
