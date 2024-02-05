# 主程序
import os
import django
from celery import Celery
from callcenter_emo.config import broker_url, result_backend


# 创建celery实例对象
app = Celery("callcenter_emo", broker=broker_url, backend=result_backend)

# 解决启动警告
app.conf.update(
    broker_connection_retry_on_startup=True,
)

# 把celery和django进行组合，识别和加载django的配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'callcenter_emo.settings')

# Django组件初始化
django.setup()

# 加载任务
# 参数必须必须是一个列表，里面的每一个任务都是任务的路径名称
# app.autodiscover_tasks(["任务1","任务2"])
app.autodiscover_tasks(["cc_celery.tasks",])

# 启动Celery的命令
# 强烈建议切换目录到cc_celery根目录下启动
# celery -A cc_celery.main worker --loglevel=info
