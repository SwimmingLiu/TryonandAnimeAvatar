import { readFileAsBase64, BaseURL, request } from '../../../utils/util.js';
const app = getApp()
// pages/index.js
Page({

    data: {
        showExample: [{
            prePath: 'https://picst.sunbangyan.cn/2023/12/31/74674eca6b54de1aeb184334112144c9.jpeg',
            postPath: 'https://picdm.sunbangyan.cn/2023/12/31/39f0b942d6e599c447f047b6c23b0aa1.jpeg',
            id: 1
        },{
            prePath: 'https://picdm.sunbangyan.cn/2023/12/31/251c95ec27b53e6c1f7fa5ecdd670e3b.jpeg',
            postPath: 'https://picst.sunbangyan.cn/2023/12/31/f38f75314b51dcb8c898c4f19559fcc7.jpeg',
            id: 2
        },{
            prePath: 'https://picst.sunbangyan.cn/2023/12/31/74674eca6b54de1aeb184334112144c9.jpeg',
            postPath: 'https://picdm.sunbangyan.cn/2023/12/31/39f0b942d6e599c447f047b6c23b0aa1.jpeg',
            id: 3
        }],
        selected_idx: 1,
        prePath: 'https://picst.sunbangyan.cn/2023/12/31/74674eca6b54de1aeb184334112144c9.jpeg',
        postPath: 'https://picdm.sunbangyan.cn/2023/12/31/39f0b942d6e599c447f047b6c23b0aa1.jpeg',
        
        leftBoxWidth: 350,
        boxWidth: 700,
        touchStartX: 0, // 触摸开始时的横坐标
        touchEndX: 0,   // 触摸结束时的横坐标

        showPopup: false,

        showLoginMask: false,
        // confirmLogin: false
    },

    // 切换样例展示
    chooseExp(e) {
        const id  = e.currentTarget.dataset.id
        for(const img of this.data.showExample) {
            if(img.id == id) {
                this.setData({
                    prePath: img.prePath,
                    postPath: img.postPath,
                    selected_idx: id
                })
                break
            }
        }
    },

    // 预览，开始拖动
    moveColumnStart(e) {
        // console.log('start');
        // console.log(e.touches[0].clientX);
        const screenWidth = wx.getSystemInfoSync().screenWidth; // 屏幕宽度，单位为 px
        const rpxValue = e.touches[0].clientX / screenWidth * 750;
        this.data.touchStartX = rpxValue
    },

    // 预览，拖动中
    moveColumn(e) {
        // console.log('move');
        // console.log(e.touches[0].clientX);
        

        const screenWidth = wx.getSystemInfoSync().screenWidth; // 屏幕宽度，单位为 px
        const rpxValue = e.touches[0].clientX / screenWidth * 750;
        this.data.touchEndX = rpxValue

        let finalX = Math.floor(this.data.leftBoxWidth + this.data.touchEndX - this.data.touchStartX)
        // console.log('$$', this.data.leftBoxWidth);
        // console.log(Math.floor(this.data.touchEndX - this.data.touchStartX));
        // console.log('#', finalX);
        if(finalX < 0) {
            finalX = 0
        }else if(finalX > this.data.boxWidth - 5) {
            finalX = this.data.boxWidth - 5
        }
        this.setData({
            leftBoxWidth: finalX
        })

        this.data.touchStartX = rpxValue
    },

    // 照片变卡通按钮
    submitImg() {
        const that = this
        wx.chooseMedia({
            count: 1, // 最多可以选择的文件个数
            mediaType: ['image'], // 选择文件的类型，可以是图片、视频或两者都可以
            sourceType: ['album', 'camera'], // 选择媒体的来源，可以是相册、拍摄或两者都可以
            camera: ['back', 'front'], // 使用前置或后置摄像头，仅在 mediaType 为 ['video'] 且 sourceType 为 ['camera'] 时有效
            success: function (res) {
              const tempFilePath = res.tempFiles[0].tempFilePath; // 选择的媒体文件的临时文件路径
              // 接下来可以对选择的媒体文件进行操作，例如上传至服务器等

              let data = {
                  userId: null,
                  imgData: null
              }
              data.userId = app.globalData.openid
              readFileAsBase64(tempFilePath)
              .then(res => {
                data.imgData = res

                console.log(data);
                // ... 上传服务器
                that.sendAnimeService(data)
              }) 
            }
          })
    },

    // 携带图片数据请求服务器，data为{user, img, img}
    sendAnimeService(data) {
        this.setData({
            showPopup: true,
        })
        const that = this
        wx.request({
            url: BaseURL + '/anime',
            method: 'POST',
            data: data,
            success: (res) => {
                console.log(res);
                const path = res.data.data.tryon_result
                that.toShowResult(path)

                that.setData({
                    showPopup: false,
                })
            },
            fail: (err) => {
                console.log(err);
                wx.showToast({
                  title: '服务失败！',
                  icon: 'error'
                })
                that.setData({
                    showPopup: false,
                })
            }
        })
    },

    toShowResult(res_url) {
        wx.navigateTo({
            url: '../../func/showResult/showResult',
            success: function(res) {
              // 通过eventChannel向被打开页面传送数据
              res.eventChannel.emit('showData', { res_url: res_url })
            }
          })
    },

    onClosePopup() {
        this.setData({
            showPopup: false
        })
    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow() {
        if(typeof this.getTabBar === 'function' && this.getTabBar()) {
          this.getTabBar().setData({
            selected: 0,
          })
        }
    },

    onLoad() {
        new Promise((resolve, reject) => {
            wx.getStorage({
                key: 'userInfo',
                success (res) {
                    const data = JSON.parse(res.data)
                    console.log("==============",data);
                    app.globalData.avatarUrl = data.avatarUrl
                    app.globalData.nickName = data.nickName
                    app.globalData.openid = data.openid
                    resolve(data)
                },
                fail(err) {
                    console.log("显示登录遮罩");
                    reject(err)
                }
            })
        }).then((res) => {
            console.log("##################", res.avatarUrl);
            if(res.openid == null || res.openid == undefined) {
                this.setData({showLoginMask: true})
            }
        }).catch(err => {
            this.setData({showLoginMask: true})
        })
        
    },

    // #################################### 登录
    // getUserProfile 手动触发，拿用户信息
    loginBtn() {
        const that = this
        console.log("login btn");
        this.setData({
            confirmLogin: true
        })
        //   获取用户信息 -- 当前是只获取头像
        new Promise((resolve, reject) => {
            wx.getUserProfile({
                lang: 'zh_CN',
                desc: '仅用于展示昵称和头像',
                success: (res) => {
                    wx.showLoading({
                      title: '正在登录',
                    })
                    console.log('getUserInfo success');
                    resolve(res.userInfo)
                },
                fail: (res) => {
                    console.log('getUserInfo fail');
                    reject(res)
                }
            })
        }).then((userInfo => {
            console.log(userInfo);
            
            app.globalData.avatarUrl = userInfo.avatarUrl
            app.globalData.nickName = userInfo.nickName
            
            return new Promise((resolve) => {
                resolve()
            })
        })).then(() => {
            that.doLogin()
        })
        
    },
    // 服务器拿密钥
    doLogin() {
        console.log("Login ...");
    
        const that = this
    
        request({
          url: BaseURL + '/getAppid',
          method: 'POST',
          data: {}
        }).then((res => {
            console.log(res);
            return new Promise((resolve, reject) => {
                resolve(res)
            })
        })).then(res => {
            // do login
            that.doLoginDetail(res.appid, res.secret)
        }).catch(err => {
            console.error(err);
        })
        },
    
    // 拿用户的openid
    doLoginDetail(appid, secret) {
        const that = this
        console.log("执行登录细节");
        wx.login({
            success: (res) => {
            console.log('success');
            // 拿到临时身份凭证 code是临时的
            if(res.code) {
                // 用户对应的openid是唯一的！
                const code = res.code
                console.log(code);
                const url = `https://api.weixin.qq.com/sns/jscode2session?appid=${appid}&secret=${secret}&js_code=${code}&grant_type=authorization_code`;
                
                wx.request({
                    url: url,
                    success: (res) => {
                        console.log(res);
                        if(res.statusCode == 200) {
                            console.log('Login success');
                            const openid = res.data.openid
                            console.log(openid);
                            app.globalData.openid = openid

                            const _data = {
                                "avatarUrl": app.globalData.avatarUrl,
                                "nickName": app.globalData.nickName,
                                "openid": app.globalData.openid
                            }

                            wx.setStorage({
                                key: 'userInfo',
                                data: JSON.stringify(_data)
                            })
                            wx.hideLoading()
                            that.setData({
                                showLoginMask: false
                            })
                        }
                    }
                })
            } else {
                console.log('获取用户登录态失败！' + res.errMsg)
            }
            }
        })
    },

    popNone() {
        wx.showToast({
          title: '啥也没有',
          icon: 'error'
        })
    },
})