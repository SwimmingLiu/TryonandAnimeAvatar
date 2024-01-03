import base64
import json
import random
import threading
import concurrent.futures
from PIL import Image
import io
import requests

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
    'cloth': f'https://i2.100024.xyz/2024/01/01/qrgivw.webp',
    'person': f'https://i2.100024.xyz/2024/01/01/qrgh9w.webp'
}
'''
https://i2.100024.xyz/2024/01/01/qrgh9w.webp
https://i2.100024.xyz/2024/01/01/qrgivw.webp
'''


def request_tryon(url, header, data):
    res = requests.post(url=url, headers=header, json=data, timeout=300)
    if res.status_code == 200:
        result_json = json.loads(res.content)
        if result_json['code'] == 200:
            base64_image_data = result_json['data']['image_value']
            # 解码 base64 数据
            decoded_image_data = base64.b64decode(base64_image_data)
            # 将二进制数据转换为图像
            print(f"success: {data['userid']}")
            # image = Image.open(io.BytesIO(decoded_image_data))
            # # print(decoded_image_data)
            # # 展示图像
            # image.show()
        else:
            print(result_json)
    else:
        print(f'请求错误: {res.status_code}')


if __name__ == "__main__":
    # Instead of starting a lone thread, manage threads in a with block
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     for i in range(10):
    #         data['userid'] = str(random.randint(0, 100000))
    #         future = executor.submit(request_tryon, url, header, data)
    #         return_value = future.result()  # If needed, to wait for thread completion
    for i in range(10):
        thread = threading.Thread(target=request_tryon, args=(url, header, data))
        thread.start()