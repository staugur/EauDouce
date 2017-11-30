/*
 * 基于https://github.com/GC0202/WordPress-connect-WeChat-applet开发
 * The MIT License (MIT)
*/

//pages/detail/detail.js
var app = getApp()
var WxParse = require('../../vender/wxParse/wxParse.js');
var utils = require('../../utils/util.js')
Page({
  data: {
    art: {},
    userInfo: {}
  },
  onPullDownRefresh: function () {
    wx.stopPullDownRefresh()
  },
  onLoad: function (options) {
  console.log('onLoad')
  var that = this
  //调用应用实例的方法获取全局数据
  app.getUserInfo(function (userInfo) {
    //更新数据
    that.setData({
      userInfo: userInfo
    })
  })
	//文章内容
    var that = this
    wx.request({
      url: app.serverUrl + '/api/wechatapplet/?' + utils.make_url({Action: 'get_blogId', blogId: options.id}),
      success: function (res) {
         var content = res.data.data.content;
         WxParse.wxParse('content', 'html', content, that,5);
         that.setData({
           info: res.data.data
         })
         wx.setNavigationBarTitle({
           title: res.data.data.title //文章页面的标题
        })
      }
    })
  },  
  onShareAppMessage: function () {
    return {
      title: this.data.userInfo.nickName + ' 推荐：' + this.data.info.title, //推荐前面是用户名字，推荐后面是文章的标题
      path: '/pages/detail/detail?id=' + this.data.info.id, //请不要修改这里
      success: function (res) {
        // 转发成功
      },
      fail: function (res) {
        // 转发失败
      }
    }
  }
})