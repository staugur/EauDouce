/*
 * 基于https://github.com/GC0202/WordPress-connect-WeChat-applet开发
 * The MIT License (MIT)
*/

//pages/index/index.js
var app = getApp()
var utils = require('../../utils/util.js')
Page({
  data: {
    list: [],
    banner: [],
    duration: 2000,
    indicatorDots: true,
    autoplay: true,
    interval: 3000,
    length: 8, //每次加载文章数量
    loading: false, //是否在加载新数据
    noMore: false, //是否还有更多数据
    plain: false
  },
  //事件处理函数
  bindViewTap: function(e) {
    wx.navigateTo({
      url: '../detail/detail?id=' + e.target.dataset.id
    })
  },
  onPullDownRefresh: function () {
    wx.stopPullDownRefresh()
  },
  onLoad: function () {
    this.index = 0;
    var that = this;
    //首页文章数据
    wx.request({
      url: app.serverUrl + '/api/wechatapplet/?' + utils.make_url({Action: 'get_index', length: that.data.length, page: that.index}),
      success: function (res) {
         that.setData({
           list: res.data.data
         })
      }
    });
    //首页轮换图数据
    wx.request({
      url: app.serverUrl + '/api/wechatapplet/?' + utils.make_url({Action: 'get_banner'}),
      success: function (res) {
         that.setData({
           banner: res.data.data
         })
      }
    });
    //调用应用实例的方法获取全局数据
    app.getUserInfo(function(userInfo){
      console.log(userInfo)
      //记录访问用户
      wx.request({
        url: app.serverUrl + '/api/wechatapplet/?' + utils.make_url({Action: 'AccessUserLog'}),
        method: 'POST',
        data: userInfo,
        header: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        success: function (res) {
          console.log(res.data)
        }
      });
    })
  },
  onShareAppMessage: function () {
    return {
      title: '陶先森de博客', //分享首页的标题
      path: '/pages/index/index',
      success: function (res) {
        // 转发成功
      },
      fail: function (res) {
        // 转发失败
      }
    }
  },
  //加载更多
  onReachBottom: function() {
      var that = this
      that.nextPage = that.index + 1;
      if(that.data.noMore == false){
          that.setData({ loading: true });
          wx.request({
            url: app.serverUrl + '/api/wechatapplet/?' + utils.make_url({Action: 'get_index', length: that.data.length, page: that.nextPage}),
            success: function (res) {
               var last = res.data.page.PageCount - 1
               if(res.data.page.page != last){
                   that.setData({
                     loading: false,
                     list: that.data.list.concat(res.data.data),
                   });
               } else {
                   that.setData({
                     loading: false,
                     noMore: true,
                   });
               }
            }
          });
          that.index++;
      }
  }
})
