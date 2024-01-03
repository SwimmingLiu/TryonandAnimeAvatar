import os
import shutil

from gpustat import select_gpu
from main import PredictModule


# 提前处理小程序中 虚拟换衣部分的样例数据

cloth_folder = 'static/cloth/'
person_folder = 'static/person/'
result_folder = 'static/result/'
cloth_lst = os.listdir(cloth_folder)
person_lst = os.listdir(person_folder)
for cloth in cloth_lst:
    for person in person_lst:
        cloth_path = cloth_folder + cloth
        person_path = person_folder + person
        person_name = person.split('.')[0]
        cloth_name = cloth.split('.')[0]
        process_foler = f"static/{cloth_name}_{person_name}"
        if not os.path.exists(process_foler):
            os.makedirs(process_foler)
        shutil.copy(cloth_path, f"{process_foler}/cloth_web.jpg")
        shutil.copy(person_path, f"{process_foler}/origin_web.jpg")
        # 虚拟换衣预计显存
        tryon_memory = 4000
        device_id = select_gpu(tryon_memory)
        main_predict = PredictModule(device_id=device_id, user_folder=process_foler)
        print("Start Tryon model... \n")
        main_predict.main()
        # 删除对象,释放GPU显存
        shutil.copy(f"{process_foler}/finalimg.png",f"{result_folder}/{cloth_name}_{person_name}.jpg")
        del main_predict
        shutil.rmtree(process_foler)
