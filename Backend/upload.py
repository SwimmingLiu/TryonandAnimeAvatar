import uuid
import qiniu
from io import BytesIO

QINIU_AK = 'nMED_cospE1W9CYhYBTwP-GI0150Gh8Mhm0vq_Zf'
QINIU_SK = '0fJs1ntpZygmAkF1gughSU6XXYHJRG0DwEG6_bsv'
QINIU_BUCKET = 'flik1337-blog'
QINIU_DOMAIN = 'oss.flik1337.com'

def get_random_filename():
    return str(uuid.uuid1())


def image2base64(localfile,filename):
    # with open(localfile, 'rb') as input_stream:
    with localfile as input_stream:
        q = qiniu.Auth(QINIU_AK, QINIU_SK)
        token = q.upload_token(QINIU_BUCKET, filename, 3600)
        ret, info = qiniu.put_data(token, filename, input_stream)
        assert ret is not None

def PIL_to_bytes(im):
    '''PIL转二进制

    :param im: PIL图像，PIL.Image
    :return: bytes图像
    '''
    bytesIO = BytesIO()
    try:
        im.save(bytesIO, format='JPEG')
    except:
        im.save(bytesIO, format='PNG')
    return bytesIO.getvalue()  # 转二进制

def upload_img(key,path):
    q = qiniu.Auth(QINIU_AK, QINIU_SK)

    token = q.upload_token(QINIU_BUCKET, key, 3600)
    ret,info = qiniu.put_file(token, key ,path)

# 使用方法
if __name__ =="__main__":
    file_name = get_random_filename()
    file_loc = r"E:\TryOnModel\flaskProject\flaskProject1\static\example\cloth_1.jpg"
    upload_img(file_name, file_loc)
    file_url = 'https://oss.flik1337.com/' + file_name # 结果

    print(file_url)