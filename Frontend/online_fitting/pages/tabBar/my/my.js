const { BaseURL, request } = require("../../../utils/util");
const app = getApp()

// pages/tabBar/my/my.js
Page({

    /**
     * 页面的初始数据
     */
    data: {
        avatarUrl: '',
        nickName: '韦龙',
    },

    onLoad() {
        this.setData({
            avatarUrl: app.globalData.avatarUrl,
            nickName: app.globalData.nickName
        })
    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow() {
        if(typeof this.getTabBar === 'function' && this.getTabBar()) {
          this.getTabBar().setData({
            selected: 2,
          })
        }
    },

    toHistory() {
        wx.navigateTo({
          url: '/pages/func/history/history',
        })
    },

    popNone() {
        wx.showToast({
          title: '啥也没有',
          icon: 'error'
        })
    },

    
})