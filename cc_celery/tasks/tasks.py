from cc_celery.main import app
import time


# 异步测试任务
@app.task
def test_task():
    print('test_task')
    time.sleep(5)
    return 'test_task'
