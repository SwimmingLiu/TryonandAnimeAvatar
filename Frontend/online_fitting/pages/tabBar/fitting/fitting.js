import { readFileAsBase64, BaseURL } from '../../../utils/util.js';
const app = getApp()
// pages/tabBar/fitting/fitting.js
Page({
    /**
     * 页面的初始数据
     */
    data: {
        swiperBanner: [{
            url: 'https://picdl.sunbangyan.cn/2023/12/31/8824342758baee235d822d0d9a6b671e.jpeg'
        },{
            url: 'https://picst.sunbangyan.cn/2023/12/31/5c22ef02d93ab56c723095ff8dd55e31.jpeg'
        },{
            url: 'https://picdm.sunbangyan.cn/2023/12/31/b16cf2aa3647692844918fe6c58e7cfc.jpeg'
        },
        ],

        // 系统自带的模特图
        person_data: [
            {
                id: 5,
                path: 'https://picdm.sunbangyan.cn/2023/12/31/c1257628ba443ad2bd64f68c3bbdef8c.jpeg',
                selected: false},
            {
                id: 4,
                path: 'https://picdm.sunbangyan.cn/2023/12/31/fcb6e1036c537d16e461d34659e7260f.jpeg',
                selected: false},
            {
                id: 3,
                path: 'https://picdm.sunbangyan.cn/2023/12/31/6a5efc22833989a767175d6965e5d189.jpeg',
                selected: false},
            {
                id: 2,
                path: 'https://picst.sunbangyan.cn/2023/12/31/3d2c2ba15dad56480784061dca36aced.jpeg',
                selected: false},
            {
                id: 1,
                path: 'https://picss.sunbangyan.cn/2023/12/31/9231294d710839f267528cc60f6a5b1a.jpeg',
                selected: false}
        ],
        currentPersonSelected: null,
        
        // 系统自带的衣服图
        cloth_data_arr: [
            {
                title: '短袖',
                data: [
                    {
                        id: 5,
                        path: 'https://picst.sunbangyan.cn/2023/12/31/99f7f6562be47564a5fff536db5c7243.jpeg',
                        selected: false},
                    {
                        id: 4,
                        path: 'https://picdl.sunbangyan.cn/2023/12/31/7f112a3eb25c3c33eff2e80def451597.jpeg',
                        selected: false},
                    {
                        id: 3,
                        path: 'https://picdl.sunbangyan.cn/2023/12/31/f07aa6e2b1ea55e1ce92bff23908c1de.jpeg',
                        selected: false},
                    {
                        id: 2,
                        path: 'https://picdm.sunbangyan.cn/2023/12/31/c77f51018067be75a1808fdd6da520ac.jpeg',
                        selected: false},
                    {
                        id: 1,
                        path: 'https://picdm.sunbangyan.cn/2023/12/31/019cbf627f6f753b0165c426c4b6616c.jpeg',
                        selected: false}
                ],
                currentClothSelected: null,
            },
    
            {
                title: '潮流',
                data: [
                    {
                        id: 1,
                        path: 'https://picst.sunbangyan.cn/2023/12/31/99f7f6562be47564a5fff536db5c7243.jpeg',
                        selected: false},
                    {
                        id: 2,
                        path: 'https://picdl.sunbangyan.cn/2023/12/31/7f112a3eb25c3c33eff2e80def451597.jpeg',
                        selected: false},
                    {
                        id: 3,
                        path: 'https://picdl.sunbangyan.cn/2023/12/31/f07aa6e2b1ea55e1ce92bff23908c1de.jpeg',
                        selected: false},
                    {
                        id: 4,
                        path: 'https://picdm.sunbangyan.cn/2023/12/31/c77f51018067be75a1808fdd6da520ac.jpeg',
                        selected: false},
                    {
                        id: 5,
                        path: 'https://picdm.sunbangyan.cn/2023/12/31/019cbf627f6f753b0165c426c4b6616c.jpeg',
                        selected: false}
                ],
                currentClothSelected: null,
            },
    
            {
                title: '长裙', 
                data: [
                    {
                        id: 1,
                        path: 'https://picst.sunbangyan.cn/2023/12/31/99f7f6562be47564a5fff536db5c7243.jpeg',
                        selected: false},
                    {
                        id: 2,
                        path: 'https://picdl.sunbangyan.cn/2023/12/31/7f112a3eb25c3c33eff2e80def451597.jpeg',
                        selected: false},
                    {
                        id: 3,
                        path: 'https://picdl.sunbangyan.cn/2023/12/31/f07aa6e2b1ea55e1ce92bff23908c1de.jpeg',
                        selected: false},
                    {
                        id: 4,
                        path: 'https://picdm.sunbangyan.cn/2023/12/31/c77f51018067be75a1808fdd6da520ac.jpeg',
                        selected: false},
                    {
                        id: 5,
                        path: 'https://picdm.sunbangyan.cn/2023/12/31/019cbf627f6f753b0165c426c4b6616c.jpeg',
                        selected: false}
                ],
                currentClothSelected: null,
            },
        ],
        // 
        active: 0,
        dynamicClass: 'normal-style',

        fileList: [
        ],

        // 这个用来标志是否读取了人物图片
        isPersonUpload: false,
        // 这个用来表示是否选择使用自己的人物照
        selectedPersonUpload: false,

        clothFileList: [],
        // 这个用来标志是否读取了  上传服饰图片
        isClothUpload: false,
        // 这个用来表示是否选择使用自己的  服饰
        selectedClothUpload: false,
        
        // 提交换装后显示的进度条遮罩
        showWaitFitting: false,

        // 这里需要计算一下
        progressWidth: '0%',
        isTimeout: false,
        intervalId: null,
    },

    // 模特卡片点击效果
    changeStyleBox(e) {
        let idx = e.currentTarget.dataset.idx
        let new_person_data = this.data.person_data
        let len = new_person_data.length
        for (let i = 0; i < len; i++) {
            // 点击的目标
            if (idx === i) {
                // 没选中，换样式
                if(this.data.currentPersonSelected == null || this.data.currentPersonSelected != idx) {
                    new_person_data[i].selected = true
                    this.setData({
                        currentPersonSelected: idx
                    })
                // 再次点击，撤销样式
                } else {
                    new_person_data[i].selected = false
                    this.setData({
                        currentPersonSelected: null
                    })
                }
            // 其余
            } else {
                new_person_data[i].selected = false
            }
          }
        
        this.setData({
            person_data: new_person_data,
            selectedPersonUpload: false
        })
    },
    // 衣服Box点击 追加边框效果
    changeStyleBoxCloth(e) {
        this.toFalseClothData()

        // console.log(e);
        let idx = e.currentTarget.dataset.scrollidx
        let tab = e.currentTarget.dataset.tabidx
        
        let cloth_data_arr = this.data.cloth_data_arr
        let new_cloth_data = cloth_data_arr[tab].data
        let len = new_cloth_data.length
        let currentClothSelected = cloth_data_arr[tab].currentPersonSelected

        for (let i = 0; i < len; i++) {
            // 点击的目标
            if (idx === i) {
                // 第一次点击or切换模特，换样式
                if(currentClothSelected == null || currentClothSelected != idx) {
                    new_cloth_data[i].selected = true
                    cloth_data_arr[tab].currentPersonSelected = idx
                    // this.setData({
                    //     currentClothSelected_1: idx,
                    // })
                // 再次点击，撤销样式
                } else {
                    new_cloth_data[i].selected = false,
                    cloth_data_arr[tab].currentPersonSelected = null
                    // this.setData({
                    //     currentClothSelected_1: null
                    // })
                }
            // 其余
            } else {
                new_cloth_data[i].selected = false
            }
        }
        cloth_data_arr[tab].data = new_cloth_data
        this.setData({
            cloth_data_arr: cloth_data_arr,
            selectedClothUpload: false
        })
         
    },

    // 删除上传的模特图片
    deleteModel(e) {
        this.setData({
            fileList: [],
            isPersonUpload: false,
            selectedPersonUpload: false
        })
    },
    // 点击上传按钮，上传人物-还没传到服务器
    readModel(e) {
        const { file } = e.detail;
        // console.log(file);
        let fileList = []
        fileList.push(file)
        // 将使用人物照的标识为true
        this.setData({
            fileList: fileList,
            isPersonUpload: true,
            selectedPersonUpload: true
        });
        this.toFalsePersonData()
    },
    // 选择某个模特，把其他的模特取消选择
    selectedRealModel(e) {
        if(this.data.isPersonUpload) {
            this.setData({
                selectedPersonUpload: true
            })
            this.toFalsePersonData()
        }
    },

    // 删除上传的衣服图片
    deleteCloth(e) {
        this.setData({
            clothFileList: [],
            isClothUpload: false,
            selectedClothUpload: false
        })
    },

    // 点击上传按钮，上传衣服-还没传到服务器
    readCloth(e) {
        const { file } = e.detail;
        // console.log(file);
        let fileList = []
        fileList.push(file)
        // 将使用人物照的标识为true
        this.setData({
            clothFileList: fileList,
            isClothUpload: true,
            selectedClothUpload: true
        });
        this.toFalseClothData()
    },

    // 选择某个衣服，把其他的衣服取消选择
    selectedRealCloth(e) {
        // console.log('click');
        if(this.data.isClothUpload) {
            if(!this.data.selectedClothUpload) {
                this.setData({
                    selectedClothUpload: true
                })
            }
            else {
                this.setData({
                    selectedClothUpload: false
                })
            }
        }
        this.toFalseClothData()
    },

    // 将系统自带的服饰图全部取消选择 
    toFalseClothData() {
        let cloth_data_arr = this.data.cloth_data_arr

        // tab
        for (let tab = 0; tab < cloth_data_arr.length; tab++) {
            for(let i = 0; i < cloth_data_arr[tab].data.length; i++) {
                cloth_data_arr[tab].data[i].selected = false
            }
        }

        this.setData({
            cloth_data_arr: cloth_data_arr
        })
    },

    // 将系统自带的人像图全部取消选择 
    toFalsePersonData() {
        // 系统自带的选择标志设置为false
        if(this.data.isPersonUpload) {
            let new_person_data = this.data.person_data
            let len = new_person_data.length
            for (let i = 0; i < len; i++) {
                new_person_data[i].selected = false
            }
            this.setData({
                person_data: new_person_data
            })
        }
    },

    // 提交按钮，整理数据，调用sendFittingService请求服务器
    SubmitBtn() {
        wx.showToast({
            title: `提交设计`,
            icon: 'none',
          });

        // 记录一下 衣服和人物
        let cloth = null;
        let person = null;
        
        // 选择系统自带的 or 选择 上传的
        if(this.data.selectedPersonUpload) {
            person = this.data.fileList
        } else {
            for(const p of this.data.person_data) {
                // console.log(p);
                if(p.selected) {
                    person = p
                    break
                }
            }
        }

        if(this.data.selectedClothUpload) {
            cloth = this.data.clothFileList
        } else {
            for(const cloths of this.data.cloth_data_arr) {
                for(const c of cloths.data) {
                    if(c.selected) {
                        cloth = c
                    }
                }
            }
        }
        
        if(this.data.selectedPersonUpload == false && person == null) {
            wx.showToast({
                title: `请选择照片`,
                icon: 'none',
              });
            return
        }
        if(this.data.selectedClothUpload == false && cloth == null) {
            wx.showToast({
                title: `请选择服饰`,
                icon: 'none',
              });
              return
        }

        // 上传的数据 若用户上传衣服和照片则转base64， 否则如果是样本图片，则只携带上样本的id
        let dataInfo = {
            userId: null,
            isUploadPerson: false,  
            isUploadCloth: false,
            personData: null,
            clothData: null,
            examplePersonId: null,
            exampleClothId: null
        }
        // 用户id 这里使用用户的唯一标识 openid
        dataInfo.userId = app.globalData.openid

        // 更新dataInfo
        let personFilePath = null
        let clothFilePath = null
        if(this.data.selectedPersonUpload){
            personFilePath = person[0].tempFilePath
            dataInfo.isUploadPerson = true
        } else {
            dataInfo.examplePersonId = person.id
        }
        if(this.data.selectedClothUpload) {
            clothFilePath = cloth[0].tempFilePath
            dataInfo.isUploadCloth = true
        }else {
            dataInfo.exampleClothId = cloth.id
        }

        this.setData({
            progressWidth: "0%"
        })
        // ... if ok show popup
        this.showWaitFitting()
        

        const that = this
        // 判断上传内容
        if(this.data.selectedClothUpload && this.data.selectedPersonUpload) {
            const that = this
            readFileAsBase64(personFilePath)
            .then(function(res) {
                dataInfo.personData = res;
                return readFileAsBase64(clothFilePath);
            })
            .then(function(res) {
                dataInfo.clothData = res; 

                console.log(dataInfo);

                // 上传至服务器等操作 !!!
                that.sendTryonService(dataInfo)
            })
            .catch(function(err) {
                console.log('读取文件失败！' + err);
            });
        } else if(this.data.selectedClothUpload) {
            readFileAsBase64(clothFilePath)
            .then(function(res) {
                dataInfo.clothData = res; 
                console.log(dataInfo);

                // 上传至服务器等操作 !!!
                that.sendTryonService(dataInfo)
            })
        } else if(this.data.selectedPersonUpload) {
            readFileAsBase64(personFilePath)
            .then(function(res) {
                dataInfo.personData = res;
                console.log(dataInfo);

                // 上传至服务器等操作 !!!
                that.sendTryonService(dataInfo)
            })
        } else {
            console.log(dataInfo);

            // 上传至服务器等操作 !!!
            that.sendTryonService(dataInfo)
        }

        
    },

    // 携带图片数据请求服务器，data为{user, img, img}
    sendTryonService(data) {
        console.log("send req");
        this.startProgressBar()
        const that = this
        wx.request({
            timeout: 60 * 1000,
            url: BaseURL + '/tryon',
            method: 'POST',
            data: data,
            success: (res) => {
                console.log(res);
                if(res.data.code != 200) {
                    wx.showToast({
                      title: '服务失败！',
                      icon: 'error'
                    })
                    return ;
                }
                const result_url = res.data.data.tryon_result
                that.toShowResult(result_url)
            },
            fail: (err) => {
                console.log(err);
                that.setData({
                    isTimeout: true
                })
                that.queryTryonResult()
                // that.closeWaitFitting()
            }
        })

    },

    startProgressBar() {
        let i = 1;
        const intervalId = setInterval(() => {
        if (i <= 83) {
            this.setData({
            progressWidth: `${i}%`
            });
            i++;
        } else {
            clearInterval(intervalId);
        }
        }, 2000);
        this.data.intervalId = intervalId
    },

    closeProgressBar() {
        clearInterval(this.data.intervalId);
        this.data.progressWidth = "0%"
    },

    // 超时进行查询
    queryTryonResult() {
        console.log("超时查询 间隔5s");
        let data = {
            userId: app.globalData.openid
        }
        const that = this
        // 超时
        wx.request({
          url: BaseURL + '/queryTryon',
          data: data,
          method: 'POST',
          success: (res) => {
            console.log(res);
            if(res.data.code==200) {
                const path = res.data.data.tryon_result   
                console.log("##########", path);
                that.toShowResult(path)
            }else {
                setTimeout(() => {
                    that.queryTryonResult()
                }, 5000)
            }
          },
          fail: (err) => {
              console.log(err);
              setTimeout(() => {
                that.queryTryonResult()
              }, 5000)
          }
        })
    },

    // 模拟换装服务完成跳转到显示结果的页面
    toShowResult(res_url) {
        this.setData({
            progressWidth: '100%'
        })
        clearInterval(this.data.intervalId)
        wx.navigateTo({
            url: '../../func/showResult/showResult',
            success: function(res) {
              // 通过eventChannel向被打开页面传送数据
              res.eventChannel.emit('showData', { res_url: res_url })
            }
          })
        
        // 关闭
        this.setData({
            isTimeout: false
        })
        this.closeProgressBar()
        this.closeWaitFitting()
    },


    // 试衣服务，等待响应的遮罩
    showWaitFitting() {
        this.setData({ showWaitFitting: true });
    },
    closeWaitFitting() {
        this.setData({ showWaitFitting: false });
    },

    // vant-tab 的标签页切换
    // 这里要把数据清空
    onChange(event) {
        // wx.showToast({
        //   title: `切换到标签 ${event.detail.name}`,
        //   icon: 'none',
        // }); 
    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow() {
        // 自定义TabBar需要
        if(typeof this.getTabBar === 'function' && this.getTabBar()) {
            this.getTabBar().setData({
              selected: 1,
            })
        };
    }
})