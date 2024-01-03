# @title Anime FaceGAN Colab app
import time
from io import BytesIO
import torch
from PIL import Image
import os

# device = "cuda" if torch.cuda.is_available() else "cpu"
# model = torch.hub.load("bryandlee/animegan2-pytorch:main", "generator", device=device).eval()
# face2paint = torch.hub.load("bryandlee/animegan2-pytorch:main", "face2paint", device=device)
# folder_path = "face_images"
# imglist = os.listdir(folder_path)
# for img in imglist:
#     img_name = img.split(".")[0]
#     img_path = folder_path + "/" + img
#     im_in = Image.open(img_path).convert("RGB")
#     im_out = face2paint(model, im_in, side_by_side=False)
#     im_out.save(folder_path + "/" + img_name + "_new.jpg")

import cv2

# 读取图片
image = cv2.imread('face_images/danielwu.jpg')

# 检查图片是否成功读取（可选）
if not os.path.exists(r'face_images/test/'):
    os.mkdir(r'face_images/test/')
if image is not None:
    # 写入图片到指定路径
    cv2.imwrite('face_images/test/danielwu.jpg', image)
else:
    print('Failed to read the image.')
