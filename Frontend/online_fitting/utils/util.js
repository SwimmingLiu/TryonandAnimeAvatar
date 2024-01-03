const BaseURL = 'https://talented-civet-separately.ngrok-free.app'

const formatTime = date => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return `${[year, month, day].map(formatNumber).join('/')} ${[hour, minute, second].map(formatNumber).join(':')}`
}

const formatNumber = n => {
  n = n.toString()
  return n[1] ? n : `0${n}`
}

// file to base64 
const readFileAsBase64 = (filePath) => {
    return new Promise((resolve, reject) => {
      wx.getFileSystemManager().readFile({
        filePath: filePath,
        encoding: 'base64',
        success: function(data) {
          resolve(data.data);
        },
        fail: function(err) {
          reject(err);
        }
      });
    });
}

// 封装 wx.request 为 Promise 形式
function request(options) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: options.url,
        method: options.method || 'GET',
        data: options.data || {},
        header: options.header || {},
        success: (res) => {
          resolve(res.data);
        },
        fail: (error) => {
          reject(error);
        }
      });
    });
}

module.exports = {
  readFileAsBase64, BaseURL, request, formatTime
}


