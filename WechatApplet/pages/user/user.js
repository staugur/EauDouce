/*
 * 基于https://github.com/GC0202/WordPress-connect-WeChat-applet开发
 * The MIT License (MIT)
*/


//pages/user/user.js
var app = getApp()
Page({
  data: {
    motto: 'Hello ! WelCome to WeChat applet',
    islogin: false,
    userInfo: {},
    version: app.globalData.version,
    gzhpic: "https://blog.saintic.com/static/img/gongzhonghao.jpg"
  },
  previewImage: function (e) {
    var current = e.target.dataset.src;
    wx.previewImage({
      current: current, // 当前显示图片的http链接
      urls: [this.data.gzhpic,] // 需要预览的图片http链接列表
    })
  },
  onPullDownRefresh: function () {
    wx.stopPullDownRefresh()
  },
  onLoad: function () {
    console.log('onLoad')
    var that = this;
    var CuserInfo = wx.getStorageSync('CuserInfo');
    if (CuserInfo.accesstoken){
      that.setData({ islogin:true });
    }
    console.log(CuserInfo)

    //调用应用实例的方法获取全局数据
    app.getUserInfo(function(userInfo){
      //更新数据
      that.setData({
        userInfo:userInfo
      })
    })
  },
  onShareAppMessage: function () {
    return {
      title: '关于我',
      path: '/pages/user/user',
      success: function (res) {
        // 转发成功
      },
      fail: function (res) {
        // 转发失败
      }
    }
  }
})
