import base64
import json
from PIL import Image
import io
import requests
public_url = "https://talented-civet-separately.ngrok-free.app"
base_url = "https://certain-ideally-foal.ngrok-free.app"
url = f"{base_url}/tryon/predict/"
header = {
    "Cache-Control": "no-cache",
    "Cookie": "abuse_interstitial=certain-ideally-foal.ngrok-free.app",
    "Pragma": "no-cache",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
data = {
    'userid': 123123,
    'cloth': f'https://talented-civet-separately.ngrok-free.app/static/example/cloth_1.jpg',
    'person': f'https://talented-civet-separately.ngrok-free.app/static/example/person_1.jpg'
}
'''
https://i2.100024.xyz/2024/01/01/qrgh9w.webp
https://i2.100024.xyz/2024/01/01/qrgivw.webp
'''
# data = {
#     "userid": 123123,
#     "origin_image": "https://i.imgs.ovh/2023/11/30/pzDEm.jpeg",
# }
print('aa')
res = requests.post(url=url, headers=header, json=data, timeout=300)
if res.status_code == 200:
    result_json = json.loads(res.content)
    if result_json['code'] == 200:
        base64_image_data = result_json['data']['image_value']
        # 解码 base64 数据
        decoded_image_data = base64.b64decode(base64_image_data)
        # 将二进制数据转换为图像
        image = Image.open(io.BytesIO(decoded_image_data))
        # print(decoded_image_data)
        # 展示图像
        image.show()
    else:
        print(result_json)
else:
    print(f'请求错误: {res.status_code}')