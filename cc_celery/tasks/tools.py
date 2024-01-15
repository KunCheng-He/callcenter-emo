# 一些基本的处理方法

import re

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


if __name__ == '__main__':
    # 测试
    data = {'id': 10, 'cs_user_id': 'http://127.0.0.1:8000/users/10/', 'upload_time': '2024-01-15T17:22:39.953363', 'file': 'http://127.0.0.1:8000/upload_files/2024/01/15/0007_OPq5Qzs.mp3'}
    print(get_upload_event_info(data))