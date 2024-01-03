import json
import shutil
import time

import requests
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import os
import sys
from AnimeGAN.model import anime_model
from AnimeGANv3.model import AnimeGANv3
from main import PredictModule
from utils import DataResult, get_image_base64, download_and_save_image, schedule_folder_deletion, get_userfolder, \
    TaskQueue
from pyngrok import ngrok
from gpustat import get_gpu_memory, select_gpu

app = Flask(__name__)
app.config.from_mapping(
    BASE_URL="http://localhost:5000",
    USE_NGROK=True
)

if app.config["USE_NGROK"]:
    # pyngrok will only be installed, and should only ever be initialized, in a dev environment

    # Get the dev server port (defaults to 5000 for Flask, can be overridden with `--port`
    # when starting the server
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else "5000"

    # Open a ngrok tunnel to the dev server
    public_url = ngrok.connect(port, domain="certain-ideally-foal.ngrok-free.app").public_url
    print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

    # Update any base URLs or webhooks to use the public ngrok URL
    app.config["BASE_URL"] = public_url

taskQueue = TaskQueue()


@app.route('/', methods=['GET', 'POST'])
def main():
    result = DataResult
    result.success()
    result.data = {
        'message': '程序端接口正常'
    }
    return result.toJson()


@app.route('/tryon/predict/', methods=['POST'])
def tryon_predict():
    result = DataResult()
    result.success()
    user_folder = None
    task_id = None
    if request.is_json:
        # 拿到结果
        req_json = request.get_data()
        try:
            req_json = req_json.decode('utf-8')
            req_json = json.loads(req_json)
            userid = str(req_json['userid'])
            user_folder = get_userfolder(userid)
            if not os.path.exists(user_folder + '/test/'):
                os.makedirs(user_folder + '/test/')
            # 复制t2到 userfoler/test路径下
            shutil.copy('static/t2.txt', user_folder + '/test/')
            # 获取衣服图
            cloth = req_json['cloth']
            cloth_path = f'{user_folder}/cloth_web.jpg'
            if not download_and_save_image(image_url=cloth, save_path=cloth_path):
                result.fail()
                return result.toJson()

            # 获取人物图
            person = req_json['person']
            person_path = f'{user_folder}/origin_web.jpg'
            if not download_and_save_image(image_url=person, save_path=person_path):
                result.fail()
                return result.toJson()
            # 任务队列
            global taskQueue
            task_memory = taskQueue.taskUsage()
            # 虚拟换衣预计显存 （预计显存 + 队列中用到的显存）
            tryon_memory = 4000 + task_memory
            device_id = select_gpu(tryon_memory)
            # 新任务插入队列中
            task_id = f"tryon_{userid}_{str(int(time.time()))}"
            taskQueue.add_task(task_id)

            main_predict = PredictModule(device_id=device_id, user_folder=user_folder)
            print("Start Tryon model... \n")
            main_predict.main()

            final_image_path = f"{user_folder}/finalimg.png"
            image_value = get_image_base64(final_image_path)
            result.data = {
                'image_value': image_value
            }
            # 删除对象,释放GPU显存
            del main_predict
            # 删除该任务
            taskQueue.delete_task(task_id)
            # 设置延迟时间（以秒为单位）
            delay_time = 300
            # 调度文件夹删除
            schedule_folder_deletion(user_folder, delay_time)
            # 返回结果
            return result.toJson()

        except Exception as e:
            result.fail()
            result.data = {
                'error': str(e)
            }
            if task_id:
                global taskQueue
                taskQueue.delete_task(task_id)
            # 调度文件夹删除
            if user_folder:
                schedule_folder_deletion(user_folder, 0)
            return result.toJson()
    else:
        result.fail()
        return result.toJson()


@app.route('/anime/predict/', methods=['POST'])
def anime_predict():
    result = DataResult()
    result.success()
    user_folder = None
    task_id = None
    if request.is_json:
        # 拿到结果
        req_json = request.get_data()
        try:
            req_json = req_json.decode('utf-8')
            req_json = json.loads(req_json)
            userid = str(req_json['userid'])
            user_folder = get_userfolder(userid)
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)
            # 获取原始图像
            origin_image = req_json['origin_image']
            origin_image_path = f'{user_folder}/anime_origin.jpg'
            if not download_and_save_image(image_url=origin_image, save_path=origin_image_path):
                result.fail()
                return result.toJson()
            final_image_path = f"{user_folder}/anime_processed.png"

            # 任务队列
            global taskQueue
            task_memory = taskQueue.taskUsage()
            # 动漫人物预计显存 （预计显存 + 队列中用到的显存）
            anime_memory = 11000 + task_memory
            device_id = select_gpu(anime_memory)
            # 新任务插入队列中
            task_id = f"anime_{userid}_{str(int(time.time()))}"
            taskQueue.add_task(task_id)
            model = AnimeGANv3(device_id)
            model.animev3_model(origin_image_path, final_image_path)
            # anime_model(origin_image_path, final_image_path)
            image_value = get_image_base64(final_image_path)
            result.data = {
                'image_value': image_value
            }
            # 删除对象,释放内存
            del model
            # 删除该任务
            taskQueue.delete_task(task_id)
            # 设置延迟时间（以秒为单位）
            delay_time = 300
            # 调度文件夹删除
            schedule_folder_deletion(user_folder, delay_time)
            # 返回结果
            return result.toJson()
        except Exception as e:
            result.fail()
            result.data = {
                'error': str(e)
            }
            if task_id:
                global taskQueue
                # 删除该任务
                taskQueue.delete_task(task_id)
            # 调度文件夹删除
            if user_folder:
                schedule_folder_deletion(user_folder, 0)
            return result.toJson()
    else:
        result.fail()
        return result.toJson()


@app.route("/gpustat/", methods=["GET", "POST"])
def gpustat():
    result = DataResult()
    result.success()
    try:
        gpu_stat = get_gpu_memory()
        result.data = {
            'gpustat': gpu_stat
        }
        return result.toJson()
    except Exception:
        result.fail()
        return result.toJson()


if __name__ == '__main__':
    app.run()
