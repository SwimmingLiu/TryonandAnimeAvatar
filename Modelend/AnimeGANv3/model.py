import cv2
import numpy as np
import onnxruntime as ort
from glob import glob
import os
import torch
import gc


class AnimeGANv3():
    def __init__(self, device=None):
        # 设置使用的gpu
        providers = [
            ('CUDAExecutionProvider', {
                'device_id': device,
            }),
            'CPUExecutionProvider',
        ]
        # 加载模型
        model = 'AnimeGANv3_Hayao_STYLE_36'  # 模型名称
        self.session = ort.InferenceSession(f'AnimeGANv3/{model}.onnx',providers=providers)


    def process_image(self, img, x8=True):
        # 图片预处理
        h, w = img.shape[:2]
        if x8:
            def to_8s(x):
                return 256 if x < 256 else x - x % 8

            img = cv2.resize(img, (to_8s(w), to_8s(h)))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32) / 127.5 - 1.0
        return img

    def load_test_data(self, image_path):
        # 加载并处理图片
        img0 = cv2.imread(image_path)
        img = self.process_image(img0)
        img = np.expand_dims(img, axis=0)
        return img, img0.shape[:2]

    def convert(self, img, scale):
        # 模型推理
        x = self.session.get_inputs()[0].name
        y = self.session.get_outputs()[0].name
        fake_img = self.session.run(None, {x: img})[0]
        images = (np.squeeze(fake_img) + 1.) / 2 * 255
        images = np.clip(images, 0, 255).astype(np.uint8)
        output_image = cv2.resize(images, (scale[1], scale[0]))
        return cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR)

    def animev3_model(self, img_input, img_output):
        print("Start AnimeGAN model... \n")
        mat, scale = self.load_test_data(img_input)
        res = self.convert(mat, scale)
        cv2.imwrite(img_output, res)


def process_images_folder(input_folder, output_folder):
    # 处理指定文件夹中的所有图片
    os.makedirs(output_folder, exist_ok=True)
    pic_form = ['.jpeg', '.jpg', '.png', '.JPEG', '.JPG', '.PNG']
    in_files = sorted(glob(f'{input_folder}/*'))
    in_files = [x for x in in_files if os.path.splitext(x)[-1] in pic_form]

    for ims in in_files:
        out_name = f"{output_folder}/{os.path.basename(ims)}"
        mat, scale = load_test_data(ims)
        res = convert(mat, scale)
        cv2.imwrite(out_name, res)


if __name__ == "__main__":
    # 使用示例
    input_folder = r'E:\TryOnModel\TryYours-Virtual-Try-On\face_images_AnimeGANv3'
    output_folder = r'E:\TryOnModel\TryYours-Virtual-Try-On\face_images_AnimeGANv3_new'
    process_images_folder(input_folder, output_folder)
