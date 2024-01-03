import os, sys
import cv2
from PIL import Image
import numpy as np
import glob
import warnings
import argparse
from cloths_segmentation.pre_trained_models import create_model

from get_cloth_mask import getClothMask
from get_densepose import getDensePose
from get_seg_grayscale import getSegGrayscal
from posenetmodel import PoseNet



class PredictModule:
    def __init__(self, device_id=None, user_folder=None,background=True):
        self.background = background
        self.device_id = None
        if device_id:
            self.device_id = device_id
        self.user_folder = user_folder

    def main(self):
        # Read input image
        user_folder = self.user_folder
        img = cv2.imread(f"{user_folder}/origin_web.jpg")
        ori_img = cv2.resize(img, (768, 1024))
        cv2.imwrite(f"{user_folder}/origin.jpg", ori_img)

        # Resize input image
        img = cv2.imread(f'{user_folder}/origin.jpg')
        img = cv2.resize(img, (384, 512))
        cv2.imwrite(f'{user_folder}/resized_img.jpg', img)

        # Get mask of cloth
        print("Get mask of cloth\n")
        clothMask_model = getClothMask(user_folder=user_folder)
        clothMask_model.getmask()

        # Get openpose coordinate using posenet
        print("Get openpose coordinate using posenet\n")
        posnet_model = PoseNet(user_folder=user_folder)
        posnet_model.run_model()

        # Generate semantic segmentation using Graphonomy-Master library
        print("Generate semantic segmentation using Graphonomy-Master library\n")
        os.chdir("./Graphonomy-master")
        terminnal_command = f"python exp/inference/inference.py --loadmodel ./inference.pth --img_path ../{user_folder}/resized_img.jpg --output_path ../ --output_name {user_folder}/resized_segmentation_img"
        os.system(terminnal_command)
        os.chdir("../")

        # Remove background image using semantic segmentation mask
        mask_img = cv2.imread(f'{user_folder}/resized_segmentation_img.png', cv2.IMREAD_GRAYSCALE)
        mask_img = cv2.resize(mask_img, (768, 1024))
        k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        mask_img = cv2.erode(mask_img, k)
        img_seg = cv2.bitwise_and(ori_img, ori_img, mask=mask_img)
        back_ground = ori_img - img_seg
        img_seg = np.where(img_seg == 0, 215, img_seg)
        cv2.imwrite(f"{user_folder}/seg_img.png", img_seg)
        img = cv2.resize(img_seg, (768, 1024))
        if not os.path.exists(f'{user_folder}/test/test/image/'):
            os.makedirs(f'{user_folder}/test/test/image/')
        cv2.imwrite(f'{user_folder}/test/test/image/00001_00.jpg', img)

        # Generate grayscale semantic segmentation image
        segGrayscal_model = getSegGrayscal(user_folder=user_folder)
        segGrayscal_model.run_model()

        # Generate Densepose image using detectron2 library
        print("\nGenerate Densepose image using detectron2 library\n")
        terminnal_command = f"python detectron2/projects/DensePose/apply_net.py dump detectron2/projects/DensePose/configs/densepose_rcnn_R_50_FPN_s1x.yaml \
        https://dl.fbaipublicfiles.com/densepose/densepose_rcnn_R_50_FPN_s1x/165712039/model_final_162be9.pkl \
        {user_folder}/origin.jpg --output {user_folder}/output.pkl -v"
        os.system(terminnal_command)

        densePose_model = getDensePose(user_folder=user_folder)
        densePose_model.run_model()

        # Run HR-VITON to generate final image
        print("\nRun HR-VITON to generate final image\n")
        os.chdir("./HR-VITON-main")
        terminnal_command = f"python3 test_generator.py --cuda True --test_name test1 --tocg_checkpoint mtviton.pth --gpu_ids 0 --gen_checkpoint gen.pth --datasetting unpaired --data_list t2.txt --dataroot ../{user_folder}/test"
        os.system(terminnal_command)

        # Add Background or Not
        l = glob.glob("./Output/*.png")

        # Add Background
        if self.background:
            for i in l:
                img = cv2.imread(i)
                img = cv2.bitwise_and(img, img, mask=mask_img)
                img = img + back_ground
                cv2.imwrite(i, img)

        # Remove Background
        else:
            for i in l:
                img = cv2.imread(i)
                cv2.imwrite(i, img)

        os.chdir("../")
        cv2.imwrite(f"{user_folder}/finalimg.png", img)


'''
/root/.cache/torch/hub/checkpoints/weights.zip
'''
