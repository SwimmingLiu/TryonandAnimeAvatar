// pages/tabBar/showResult/showResult.js
Page({

    /**
     * 页面的初始数据
     */
    data: {
        resPath: ''
    },

    onLoad: function(){
        const that = this
        const eventChannel = this.getOpenerEventChannel()
        // 监听acceptDataFromOpenerPage事件，获取上一页面通过eventChannel传送到当前页面的数据
        eventChannel.on('showData', function(data) {
          console.log(data)
          const imgUrl = data.res_url
          that.setData({
            resPath: imgUrl
          })
        })
      },

      saveToPhone() {
          const url = this.data.resPath
        // 下载图片到本地临时文件
        wx.downloadFile({
            url: url, // 将图片地址替换为对应的 URL
            success: function(res) {
            // 下载成功后的临时文件路径
            var tempFilePath = res.tempFilePath;
            
            // 保存图片到相册
            wx.saveImageToPhotosAlbum({
                filePath: tempFilePath,
                success: function(res) {
                console.log('保存成功');
                },
                fail: function(error) {
                console.log('保存失败', error);
                }
            });
            },
            fail: function(error) {
            console.log('下载失败', error);
            }
        });
      },

      popNone() {
          wx.showToast({
            title: '啥也没有',
            icon: 'error'
          })
      }
})

