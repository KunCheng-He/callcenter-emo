import os
import time
from urllib.parse import urlparse

from cc_celery.main import app
from .tools import get_upload_event_info, unzip_file, mp3_add_database, cut_audio_save
from .ai_ser.recognition import recognize_sentiment
from apps.audio.models import Audio, AudioPart
from apps.emotion.models import Emotion
from apps.accounts.models import CustomUser
from apps.ser_model.models import SERModel


@app.task
def audio_process(upload_dict: dict):
    """
    根据上传事件得到的实例，处理上传文件，加入音频表中
    """
    # 获取上传事件实例中的数据
    event_id, cs_user_id, file_path, model_id  = get_upload_event_info(upload_dict)
    # 还原完整文件路径
    file_full_path = os.path.join(os.getcwd(), "upload_files", file_path)
    # 获取文件类型，根据类型不同进行不同处理
    _, file_type = os.path.splitext(file_path)
    if file_type == '.mp3':
        # 处理mp3格式的文件
        audio_id = mp3_add_database(event_id, file_full_path, cs_user_id)
        # 识别音频情感
        emotion_recognition.delay(audio_id, cs_user_id, model_id)
        return f"event_id:{event_id} audio add database, filename:{file_path}"
    elif file_type == '.zip':
        # 处理zip格式的文件
        unzip_path = unzip_file(file_full_path)
        for root, dirs, files in os.walk(unzip_path):
            for file in files:
                if file.endswith('.mp3'):
                    mp3_file_path = os.path.join(root, file)
                    audio_id = mp3_add_database(event_id, mp3_file_path, cs_user_id)
                    # 识别音频情感
                    emotion_recognition.delay(audio_id, cs_user_id, model_id)
        return f"event_id:{event_id} zip file unzip and audio add database, zipname:{file_path}"
    else:
        # 其他格式的文件代表有误
        print("文件格式不在处理范围")
        return "文件格式不在处理范围"


@app.task
def emotion_recognition(audio_id: int, user_id: int, model_id: int):
    """
    情感识别任务，根据给定的音频id进行情感识别，并将结果写入情感数据库
    """
    # 获取音频实例和文件的完整路径
    audio_object = Audio.objects.get(id=audio_id)
    left_path = os.path.join(os.getcwd(), audio_object.left_file_path[1:])
    right_path = os.path.join(os.getcwd(), audio_object.right_file_path[1:])
    # 获取模型完整路径
    ser_model = SERModel.objects.get(id=model_id)
    model_path = os.path.join(os.getcwd(), str(ser_model.path))
    # 情感识别
    left_emotions = recognize_sentiment(left_path, model_path)
    right_emotions = recognize_sentiment(right_path, model_path)
    frame_num = len(left_emotions)
    # 写入情感数据库
    emotion_object = Emotion.objects.create(
        audio_id = audio_object,
        frame_num = frame_num,
        left_emotions = left_emotions,
        right_emotions = right_emotions
    )
    emotion_object.save()
    # 统计情感信息更新到客服的用户信息中
    user_object = CustomUser.objects.get(id=user_id)
    user_object.user_emo_up = user_object.user_emo_up + left_emotions.count(0)
    user_object.user_emo_norm = user_object.user_emo_norm + left_emotions.count(1)
    user_object.user_emo_down = user_object.user_emo_down + left_emotions.count(2)
    user_object.emo_up = user_object.emo_up + right_emotions.count(0)
    user_object.emo_norm = user_object.emo_norm + right_emotions.count(1)
    user_object.emo_down = user_object.emo_down + right_emotions.count(2)
    user_object.save()
    return f"audio_id:{audio_id} emotion recognition success, add to emotion database, emotion_id:{emotion_object.id}"


@app.task
def audio_cut(ori_data: dict):
    # 提取ID获取原始音频片段实例
    audio_part_id = int(urlparse(ori_data['url']).path.split('/')[-2])
    part_obj = AudioPart.objects.get(id=audio_part_id)
    # 截取片段并更新数据
    save_path = cut_audio_save(part_obj.cut_audio_path, part_obj.start_time, part_obj.end_time)
    part_obj.part_path = save_path
    part_obj.save()
    # 更新用户剪辑片段数
    user = part_obj.user_id
    user.cut_num = user.cut_num + 1
    user.save()
    return f"audio_part_id:{audio_part_id} cut success, save_path:{save_path}"
