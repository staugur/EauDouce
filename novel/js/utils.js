/*
    Public Utils
*/

"use strict";

var API_URL = "/api/novel/?";
var version = "v1";
var accesskey_id = "U2JpQXBp";
var accesskey_secret = "GBRDOOBSGIZGIZBZHE2TINJYGZQTKY3B";

var Util = (function () {
    var prefix = 'eaudouce_';
    var StorageGetter = function (key) {
        return localStorage.getItem(prefix + key);
    }
    var StorageSetter = function (key, val) {
        return localStorage.setItem(prefix + key, val);
    }
    var getUrlQuery = function (key, acq) {
        /*
            获取URL中?之后的查询参数，不包含锚部分，比如url为http://blog.saintic.com/?status=1&Action=getCount
            若无查询的key，则返回整个查询参数对象，即返回{status: "1", Action: "getCount"}；
            若有查询的key，则返回对象值，返回值可以指定默认值acq：如key=status, 返回1；key=test返回acq
        */
        var str = location.search;
        var obj = {};
        if (str) {
            str = str.substring(1, str.length);
            // 以&分隔字符串，获得类似name=xiaoli这样的元素数组
            var arr = str.split("&");
            //var obj = new Object();
            // 将每一个数组元素以=分隔并赋给obj对象
            for (var i = 0; i < arr.length; i++) {
                var tmp_arr = arr[i].split("=");
                obj[decodeURIComponent(tmp_arr[0])] = decodeURIComponent(tmp_arr[1]);
            }
        }
        return key ? obj[key] || acq : obj;
    }
    var formatUnixtimestamp = function (unixtimestamp) {
        //时间戳转化为日期格式
        var unixtimestamp = new Date(unixtimestamp * 1000);
        var year = 1900 + unixtimestamp.getYear();
        var month = "0" + (unixtimestamp.getMonth() + 1);
        var date = "0" + unixtimestamp.getDate();
        var hour = "0" + unixtimestamp.getHours();
        var minute = "0" + unixtimestamp.getMinutes();
        var second = "0" + unixtimestamp.getSeconds();
        return year + "-" + month.substring(month.length - 2, month.length) + "-" + date.substring(date.length - 2, date.length) +
            " " + hour.substring(hour.length - 2, hour.length) + ":" +
            minute.substring(minute.length - 2, minute.length) + ":" +
            second.substring(second.length - 2, second.length);
    }

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
        return md5(canonicalizedQueryString).toUpperCase();
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
        // 设置公共参数
        var publicParams = {
            accesskey_id: accesskey_id,
            version: version,
            timestamp: timestamp
        };
        // 添加加公共参数
        for (var i in publicParams) {
            params[i] = publicParams[i];
        }
        var uri = ''
        for (var i in params) {
            uri += i + '=' + params[i] + '&';
        }
        uri += 'signature=' + _sign(params);
        return uri
    }

    return {
        StorageGetter: StorageGetter,
        StorageSetter: StorageSetter,
        getUrlQuery: getUrlQuery,
        formatUnixtimestamp: formatUnixtimestamp,
        make_url: make_url
    }
})();