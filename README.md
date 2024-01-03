# Tryon and Anime Avatar

## Introduction

基于HR-VITON的虚拟换衣 (Tryon) 和AnimeGANv3的动漫人物 (Anime Avatar) 小程序

<img src="https://s11.ax1x.com/2024/01/03/pijbxeS.png" alt="image-20240103150359944" width=250px/>  <img src="https://s11.ax1x.com/2024/01/03/pijqCJs.png" alt="image-20240103144948278" width=250px />  <img src="https://s11.ax1x.com/2024/01/03/pijqPWn.png" alt="image-20240103145035829" width=250px />

<img src="https://s11.ax1x.com/2024/01/03/pijbzdg.png" alt="image-20240103145144985" style="width=200px;" width=250px/><img src="https://s11.ax1x.com/2024/01/03/pijq9ij.png" alt="image-20240103150707136" style="width=200px;" width=250px/><img src="https://s11.ax1x.com/2024/01/03/pijqSoQ.png" alt="image-20240103150330684" style="width=200px;" width=250px/>


## Workflow

### DataBase

MysqlDataBase： Tryon 和 Anime Avatar 任务分别创建表，记录用户id、处理结果、任务状态等信息

### Frontend

1. 用户进入小程序会判断是否登录过，未登录，则弹出登录页面
2. 主页包括动漫化效果展示模块，和实现上传图片动漫化功能按钮，最后显示处理结果；
3. 换衣页面包括轮播图展示效果图，用户可以选择系统自带的模特和服饰图片或者自己上传图片进行在线试衣功能，最后显示结果；
4. 个人信息页面显示用户头像和昵称，下面包括用户的历史操作记录，用户可以点击跳转查看；
5. 历史记录页面将显示用户所有的操作记录

### Backend

1. 接收来自前端的请求，获取用户的userid以及待处理的图片数据。
2. 建立数据库，用来存储用户信息以及用户操作。
3. 将用户的数据、具体操作、时间以及处理结果状态传入MySQL数据库。对于默认未处理的数据，处理结果状态设为0，表示尚未完成处理。
4. 根据前段请求的功能，将数据传入对应的模型端服务器。
5. 将待处理的图片数据传送至模型端进行处理，并等待接收模型端的处理结果。
6. 在数据库中修改此次操作对应的数据处理状态为1，表示图片已经完成处理。
7. 将查询结果返回给前端。
8. 若前端请求超时，前端可以轮训访问重传函数，查询数据处理状态。数据处理完成后，将处理好的数据进行重传。
9. 将查询结果返回给前端。

### Modelend

**动态调度**：

1. TaskQueue记录Tryon 和 Anime Avatar任务
2. 每次调用模型前，获取GPU显存剩余容量
3. 如果显存足够则调用模型，否则返回显存不足响应

#### Tryon Model

1. **flask框架**：通过接口获取衣服图片和人物图片
2. 调用`getClothMask`函数生成服装掩码。
3. 利用PoseNet模型来获取图像中人物的姿势坐标。
4. 在`Graphonomy-master`目录下运行命令行脚本，生成人物照片的语义分割。
5. 使用语义分割掩码去除人物图像背景。
6. 调用`getSegGrayscal`函数生成灰度语义分割图像。
7. 通过DensePose库生成人物姿态图像。
8. 调用HR-VITON网络生成最终的合成图像。
9. 保存处理后的图像，然后响应请求。

#### Anime Avatar

1. 通过接口获取人像图片
2. 预处理图像，调整尺寸大小和色域，适应模型输入
3. 使用 AnimeGANv3 模型进行推理，并将输出图像调整回原始尺寸和原域。
4. 保存处理后的图像，然后响应请求

### WorkFlow Graph

![workflow graph](E:\研究生\程序设计课程\Pictures\流程图.png)

## Frame

### DataBase

[![MySQL](https://img.shields.io/badge/MySQL-test?style=for-the-badge&logo=mysql&logoColor=white&color=blue)](https://www.mysql.com/)

### Frontend

[![wechat mini programs](https://img.shields.io/badge/wechat%20mini%20programs-test?style=for-the-badge&logo=wechat&logoColor=white&color=%2320B2AA)](https://developers.weixin.qq.com/)

### Backend

[![Python](https://img.shields.io/badge/python-3776ab?style=for-the-badge&logo=python&logoColor=ffd343)](https://www.python.org/)[![Flask](https://img.shields.io/badge/flask-3e4349?style=for-the-badge&logo=flask&logoColor=ffffff)](https://flask.palletsprojects.com/)[![Pytorch](https://img.shields.io/badge/PYtorch-test?style=for-the-badge&logo=pytorch&logoColor=white&color=orange)](https://pytorch.org/)[![Ngrok](https://img.shields.io/badge/NGROK-test?style=for-the-badge&logo=NGROK&logoColor=white&color=blue)](https://flask.palletsprojects.com/)

## Reference

### ModelEnd

[**HR-VITON**](https://github.com/sangyun884/HR-VITON)

[**Posenet**](https://github.com/rwightman/posenet-python)

[**Graphonomy**](https://github.com/Gaoyiminggithub/Graphonomy)

**[detectron2](https://github.com/facebookresearch/detectron2)**

[**cloth image segmentation**](https://github.com/ternaus/cloths_segmentation)

[**TryYours-Virtual-Try-On**](https://github.com/lastdefiance20/TryYours-Virtual-Try-On)

[**AnimeGANv3**](https://github.com/TachibanaYoshino/AnimeGANv3)

