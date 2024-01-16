import os
import time

from cc_celery.main import app
from .tools import get_upload_event_info, mp3_separate_left_right, get_relative_path
from apps.audio.models import Audio
from apps.upload_events.models import UploadEvent


# 异步测试任务
@app.task
def test_task():
    print('当前程序执行路径', os.getcwd())
    time.sleep(5)
    return 'test_task'


@app.task
def audio_process(upload_dict: dict):
    """
    根据上传事件得到的实例，处理上传文件，加入音频表中
    """
    # 获取上传事件实例中的数据
    event_id, cs_user_id, file_path = get_upload_event_info(upload_dict)
    # 还原完整文件路径
    file_full_path = os.path.join(os.getcwd(), "upload_files", file_path)
    # 获取文件类型，根据类型不同进行不同处理
    _, file_type = os.path.splitext(file_path)
    if file_type == '.mp3':
        # 处理mp3格式的文件为wav格式的文件
        left_path, right_path = mp3_separate_left_right(file_full_path)
        # 获取上传事件实例
        upload_object = UploadEvent.objects.get(id=event_id)
        # 将分离出的音频加入音频数据表
        audio_object = Audio.objects.create(
            orig_file_path = get_relative_path(file_full_path, os.getcwd()),
            left_file_path = get_relative_path(left_path, os.getcwd()),
            right_file_path = get_relative_path(right_path, os.getcwd()),
            upload_event_id = upload_object
        )
        audio_object.save()
        return f"event_id:{event_id} audio add database, filename:{file_path}"
    elif file_type == '.zip':
        # 处理zip格式的文件
        return "zip"
    else:
        # 其他格式的文件代表有误
        print("文件格式不在处理范围")
        return "文件格式不在处理范围"
