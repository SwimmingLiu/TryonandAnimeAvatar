// pages/func/history/history.js
import { request, BaseURL, formatTime } from '../../../utils/util.js';
const app = getApp()

Page({

    /**
     * 页面的初始数据
     */
    data: {
        record: [],
    },

    onLoad() {
        const that = this
        request({
            url: BaseURL + '/getHistory',
            method: 'POST',
            data: {
                userId: app.globalData.openid
            }
        }).then(res => {
            console.log(res);
            const data = res.data
            
            for(let item of data) {
                item['width'] = '100%'
                item['loaded'] = false
                let _time = new Date(item.time * 1000)
                // console.log(_time);
                item['time'] = formatTime(_time)
            }
            // console.log(data);

            that.setData({
                record: data
            })
        }).catch(err => {
            console.log(err);
        })
    },

    // 修改图片尺寸
    updateImgSize() {
        const query = wx.createSelectorQuery().in(this);
            const that = this
            query.selectAll('.qImg').boundingClientRect((rects) => {
            if (rects) {
                rects.forEach((rect, index) => {
                    // 获取每个元素的宽度和高度
                    const width = rect.width;
                    const height = rect.height;
                    // console.log(width, height, index);

                    // 根据条件判断是否需要重新设置宽高
                    let newWidth = null;
                    if (width - height > 100) {
                        newWidth = '700rpx'; // 新的宽度
                    } else {
                        newWidth = '350rpx'; // 新的宽度
                    }
                    let record = that.data.record
                    record[index].width = newWidth
                    that.setData({
                        record: record
                    })
                });
            }
            }).exec();
    },

    // 图片加载完毕回调设置标记为true
    loadedImg(e) {
        const index = e.currentTarget.dataset.index
        console.log("加载完成 ", index);
        this.data.record[index].loaded = true
        if(this.checkAllImgLoaded()) {
            this.updateImgSize()
        }
    },

    // 检查图片是否全部加载完毕
    checkAllImgLoaded() {
        let mark = true
        this.data.record.forEach(rc => {
            if(rc.loaded == false) {
                mark = false
            }
        })

        return mark
    },

    // 很垃圾，又加载了一遍
    previewImage(e) {
        console.log(e);
        const url = e.currentTarget.dataset.url 
        wx.previewImage({
          urls: [url],
        })
    }
})