import pymysql
import requests
from flask import request, Flask
from flask_cors import CORS
from flask import jsonify
import base64
import os
from io import BytesIO
from PIL import Image
import datetime

from utils import DatabaseManager, getImgUrl

app = Flask(__name__)
CORS(app)
public_url = "https://talented-civet-separately.ngrok-free.app"
url = 'https://certain-ideally-foal.ngrok-free.app'
result_path = 0

db_manager = DatabaseManager('localhost', 'root', 'root', 'tryon')


# 换衣超时，小程序每隔5s调用一次此函数
@app.route("/queryTryon", methods=['POST'])
def queryTryon():
    global db_manager
    # 已传userId
    try:
        data = request.get_json()
        user_id = str(data.get('userId'))
        resutl_url = db_manager.query_return('tryon', user_id)[0]
        if resutl_url[3] == 1:
            return jsonify({'code': 200, 'msg': 'success', 'data': {'tryon_result': resutl_url[1]}})
        else:
            return jsonify({'code': 500, 'msg': 'fail'})
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)})


# 微信登录密钥
@app.route("/getAppid", methods=['POST'])
def getAppid():
    data = {'appid': 'wx27b048d6cb00578a',
            'secret': 'df319949ed37cff1b8d262c12c2c791b'}

    return jsonify(data)


@app.route("/getHistory", methods=['POST'])
def getHistory():
    # 已传userId
    global db_manager
    res = []
    try:
        data = request.get_json()
        user_id = str(data.get('userId'))
        resutl_url_tryon = db_manager.query_records('tryon', user_id)
        resutl_url_anime = db_manager.query_records('anime', user_id)
        for i in resutl_url_tryon:
            if i[3] == 1:
                status = '已完成'
                res.append({'op': '虚拟换衣', 'time': i[2], 'result_url': i[1], 'status': status})
        for i in resutl_url_anime:
            if i[3] == 1:
                status = '已完成'
                res.append({'op': '动漫人物', 'time': i[2], 'result_url': i[1], 'status': status})
        data = {
            "code": 200,
            "msg": 'success',
            "data": res
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)})


def save_image_from_base64(base64_string, filename, id):
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    save_path = './static/' + filename + '/'
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    save_path = save_path + id + '.jpg'
    image.save(save_path)
    # image.show()


@app.route('/tryon', methods=['GET', 'POST'])
def tryon():
    global db_manager
    try:
        # 接受前端
        result = 0
        data = request.get_json()
        personData = data.get('personData')
        clothData = data.get('clothData')
        user_id = str(data.get('userId'))
        print(user_id)
        isUploadCloth = data.get('isUploadCloth')
        isUploadPerson = data.get('isUploadPerson')
        exampleCothId = str(data.get('exampleClothId'))
        examplePersonId = data.get('examplePersonId')

        now = datetime.datetime.now()
        now_timestamp = str(now.timestamp())
        now = str(now)
        # 数据库存入当前任务
        db_manager.add_record('tryon', f'{user_id}', '', now_timestamp, 0)
        time = ''
        now = now[11:19]
        for i in range(len(now)):
            if now[i] == ':':
                time += '_'
            else:
                time += now[i]
        result_path = None
        if not isUploadPerson and not isUploadCloth:
            result_path = f'static/result/cloth_{str(exampleCothId)}_person_{str(examplePersonId)}.png'
            result_path = getImgUrl(result_path)
            result = {
                'code': 200,
                'msg': 'success',
                'data': {
                    'tryon_result': result_path
                }
            }
        else:
            if not isUploadCloth:
                clothData_path = 'static/example/cloth_' + str(exampleCothId) + '.jpg'
                clothData_path = getImgUrl(clothData_path)
            else:
                save_image_from_base64(clothData, 'tryon/cloths', f"{user_id}_{time}")
                clothData_path = 'static/tryon/cloths/' + str(user_id) + '_' + time + '.jpg'
                clothData_path = getImgUrl(clothData_path)
            if not isUploadPerson:
                personData_path = 'static/example/person_' + str(examplePersonId) + '.jpg'
                personData_path = getImgUrl(personData_path)
            else:
                save_image_from_base64(personData, 'tryon/persons', f"{user_id}_{time}")
                personData_path = 'static/tryon/persons/' + str(user_id) + '_' + time + '.jpg'
                personData_path = getImgUrl(personData_path)

            # 请求模型端
            data = {
                'userid': data.get('userId'),
                'person': personData_path,
                'cloth': clothData_path,
            }

            headers = {
                "Cache-Control": "no-cache",
                "Cookie": "abuse_interstitial=certain-ideally-foal.ngrok-free.app",
                "Pragma": "no-cache",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            }

            result_file = user_id + time
            tryon_url = url + "/tryon/predict/"
            response = requests.post(url=tryon_url, json=data, headers=headers)
            res = response.json()

            save_image_from_base64(res['data']['image_value'], 'tryon/result', result_file)

            result_path = 'static/tryon/result/' + result_file + '.jpg'
            result_path = getImgUrl(result_path)
            result = {
                'code': res['code'],
                'msg': res['msg'],
                'data': {
                    'tryon_result': result_path
                }
            }
        db_manager.update_record('tryon', f"{user_id}", now_timestamp, 1, result_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({'code': 500, 'msg': '服务器错误', 'data': {'error': str(e)}})


@app.route('/anime', methods=['GET', 'POST'])
def anime():
    global db_manager
    try:
        data = request.get_json()
        origin_image = data.get('imgData')
        user_id = str(data.get('userId'))
        save_image_from_base64(origin_image, 'anime/origin_image', user_id)
        origin_image_path = 'static/anime/origin_image/' + str(user_id) + '.jpg'
        origin_image_path = getImgUrl(origin_image_path)
        now = datetime.datetime.now()
        now_timestamp = str(now.timestamp())
        now = str(now)
        # 数据库存入当前任务
        db_manager.add_record('anime', f'{user_id}', '', now_timestamp, 0)
        data = {
            'userid': data.get('userId'),
            'origin_image': origin_image_path,
        }
        headers = {
            "Cache-Control": "no-cache",
            "Cookie": "abuse_interstitial=certain-ideally-foal.ngrok-free.app",
            "Pragma": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        anime_url = url + '/anime/predict/'
        response = requests.post(url=anime_url, json=data, headers=headers)
        res = response.json()
        time = ''
        now = now[11:19]
        for i in range(len(now)):
            if now[i] == ':':
                time += '_'
            else:
                time += now[i]
        result_file = user_id + time
        save_image_from_base64(res['data']['image_value'], 'anime/result', result_file)
        result_path = getImgUrl('static/anime/result/' + result_file + '.jpg')
        result = {
            'code': res['code'],
            'msg': res['msg'],
            'data': {
                'tryon_result': result_path
            }
        }
        db_manager.update_record('anime', f"{user_id}", now_timestamp, 1, result_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({'code': 500, 'msg': '服务器错误', 'data': {'error': str(e)}})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8989, debug=False)
