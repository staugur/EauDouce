/*
 * 基于https://github.com/GC0202/WordPress-connect-WeChat-applet开发
 * The MIT License (MIT)
*/

//pages/utils/util.js
var MD5 = require('./md5.js');
var version = "v1";
var accesskey_id = "U2JpQXBp";
var accesskey_secret = "GBRDOOBSGIZGIZBZHE2TINJYGZQTKY3B";
function _sign(params) {
    /*
        @params object: uri请求参数(包含除signature外的公共参数)
    */
    if (typeof (params) != "object") {
        console.error("params is not an object");
        return false;
    }
    // NO.1 参数排序
    var _my_sorted = Object.keys(params).sort();
    // NO.2 排序后拼接字符串
    var canonicalizedQueryString = '';
    for (var _i in _my_sorted) {
        canonicalizedQueryString += _my_sorted[_i] + '=' + params[_my_sorted[_i]] + '&';
    }
    canonicalizedQueryString += accesskey_secret
    // NO.3 加密返回签名: signature
    return MD5.hexMD5(canonicalizedQueryString).toUpperCase();
}
function make_url(params) {
    /*
        @params object: uri请求参数(不包含公共参数)
    */
    if (typeof (params) != "object") {
        console.warn("params is not an object, set {}");
        var params = {};
    }
    // 获取当前时间戳
    var timestamp = Math.round(new Date().getTime() / 1000 - 5).toString();
    //console.log(timestamp);
    // 设置公共参数
    var publicParams = { accesskey_id: accesskey_id, version: version, timestamp: timestamp };
    // 添加加公共参数
    for (var i in publicParams) {
        params[i] = publicParams[i];
    }
    var uri = ''
    for (var i in params) {
        uri += i + '=' + params[i] + '&';
    }
    uri += 'signature=' + _sign(params);
    console.log(uri);
    return uri
}
function formatTime(date) {
  var year = date.getFullYear()
  var month = date.getMonth() + 1
  var day = date.getDate()

  var hour = date.getHours()
  var minute = date.getMinutes()
  var second = date.getSeconds()


  return [year, month, day].map(formatNumber).join('/') + ' ' + [hour, minute, second].map(formatNumber).join(':')
}

function formatDate(date, split) {
  var year = date.getFullYear()
  var month = date.getMonth() + 1
  var day = date.getDate()
  return [year, month, day].map(formatNumber).join(split || '')
}


function formatNumber(n) {
  n = n.toString()
  return n[1] ? n : '0' + n
}

module.exports = {
  formatTime: formatTime,
  formatDate: formatDate,
  make_url: make_url
}
