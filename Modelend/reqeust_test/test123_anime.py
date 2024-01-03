import base64
import json
from PIL import Image
import io
import requests
base_url = "https://certain-ideally-foal.ngrok-free.app"
url = f"{base_url}/anime/predict/"
header = {
    "Cache-Control": "no-cache",
    "Cookie": "abuse_interstitial=certain-ideally-foal.ngrok-free.app",
    "Pragma": "no-cache",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
# data = {
#     'userid': 123123,
#     'cloth': 'https://i.imgs.ovh/2023/11/29/pc0GN.jpeg',
#     'person': 'https://i.imgs.ovh/2023/11/29/pcIpR.jpeg'
# }
'''
https://i.imgs.ovh/2023/12/13/mRvAA.jpeg
https://i.imgs.ovh/2023/12/13/mRN8o.jpeg
https://i.imgs.ovh/2023/12/13/mRys5.jpeg
https://i.imgs.ovh/2023/12/13/mcCis.jpeg
https://i.imgs.ovh/2023/12/13/mcVVX.jpeg
https://i.imgs.ovh/2023/12/13/mcLWU.jpeg
'''
data = {
    "userid": 123123,
    "origin_image": "https://i2.100024.xyz/2024/01/01/qrgh9w.webp",
}
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