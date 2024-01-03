import base64
import json
import shutil
import time
from threading import Timer

import requests
from PIL import Image
from io import BytesIO


class DataResult():
    def __init__(self, code=200, msg='success', data=None):
        self.code = code
        self.msg = msg
        self.data = data

    def success(self, data=None):
        self.code = 200
        self.msg = 'success'
        self.data = data

    def fail(self, data=None):
        self.code = 500
        self.msg = 'fail'
        if data is None:
            self.data = ''
        else:
            self.data = data

    def toJson(self):
        return json.dumps(self.__dict__)


class TaskQueue():
    def __init__(self):
        self.tasks = list()

    def add_task(self, task_id):
        self.tasks.append(task_id)

    def delete_task(self, task_id):
        self.tasks.remove(task_id)

    def taskUsage(self):
        gpu_memory = 0
        for task in self.tasks:
            task_name = task.split("_")[0]
            if str(task_name) is "tryon":
                gpu_memory += 4000
            else:
                gpu_memory += 11000
        return gpu_memory

def get_image_base64(image_path):
    with open(image_path, 'rb') as file:
        binary_content = file.read()
    return base64.b64encode(binary_content).decode('utf-8')


def download_and_save_image(image_url, save_path):
    # 发送请求下载图片
    response = requests.get(image_url)
    if response.status_code == 200:
        # 将内容转换为二进制流
        image_data = BytesIO(response.content)
        # 打开图片
        image = Image.open(image_data)
        # 将图片转换为 JPG 格式（如果需要）
        if image.format != 'JPEG':
            image = image.convert('RGB')
        # 保存图片
        image.save(save_path, format='JPEG')
        return True
    else:
        return False


def delete_folder(folder_path):
    shutil.rmtree(folder_path, ignore_errors=True)


def schedule_folder_deletion(folder_path, delay):
    deletion_timer = Timer(delay, delete_folder, args=(folder_path,))
    deletion_timer.start()


def get_userfolder(user_id):
    # 获取用户id
    userid = str(user_id)
    # 获取当前时间戳
    date_now = str(int(time.time()))
    user_folder = 'static/' + userid + '_' + date_now
    return user_folder
