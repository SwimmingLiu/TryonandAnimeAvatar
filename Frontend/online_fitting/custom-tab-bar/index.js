Component({
  properties: {

  },
  data: {
    "selected": 0,
    "backgroundColor": "#FFFFFF",
    "color": "#979795",
    "selectedColor": "#1c1c1b",
    "list": [{
      "pagePath": "/pages/tabBar/index/index",
      "iconPath": "/custom-tab-bar/icon/index.svg",
      "selectedIconPath": "/custom-tab-bar/icon/index_selected.svg",
      "text": "首页"
    }, {
      "pagePath": "/pages/tabBar/fitting/fitting",
      "iconPath": "/custom-tab-bar/icon/dress.svg",
      "selectedIconPath": "/custom-tab-bar/icon/dress_selected.svg",
      "isSpecial": true,
      "text": "试衣"
    }, {
      "pagePath": "/pages/tabBar/my/my",
      "iconPath": "/custom-tab-bar/icon/my.svg",
      "selectedIconPath": "/custom-tab-bar/icon/my_selected.svg",
      "text": "我的"
    }]
  },
  methods: {
    switchTab(e) {
      const data = e.currentTarget.dataset;
      const url = data.path;
      wx.switchTab({url});
    }
  }
})