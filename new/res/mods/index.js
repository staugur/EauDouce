/**

 @Name: Fly社区主入口

 */
 

layui.define(['carousel','layer', 'laytpl', 'form', 'element', 'upload', 'util'], function(exports){
  
  var $ = layui.jquery
  ,layer = layui.layer
  ,laytpl = layui.laytpl
  ,form = layui.form
  ,element = layui.element
  ,upload = layui.upload
  ,util = layui.util
  ,carousel = layui.carousel
  ,device = layui.device()

  ,DISABLED = 'layui-btn-disabled';
  
  //阻止IE7以下访问
  if(device.ie && device.ie < 8){
    layer.alert('如果您非得使用 IE 浏览器访问Fly社区，那么请使用 IE8+');
  }
  
  layui.focusInsert = function(obj, str){
    var result, val = obj.value;
    obj.focus();
    if(document.selection){ //ie
      result = document.selection.createRange(); 
      document.selection.empty(); 
      result.text = str; 
    } else {
      result = [val.substring(0, obj.selectionStart), str, val.substr(obj.selectionEnd)];
      obj.focus();
      obj.value = result.join('');
    }
  };


  //数字前置补零
  layui.laytpl.digit = function(num, length, end){
    var str = '';
    num = String(num);
    length = length || 2;
    for(var i = num.length; i < length; i++){
      str += '0';
    }
    return num < Math.pow(10, length) ? str + (num|0) : num;
  };
  
  var fly = {

    //Ajax
    json: function(url, data, success, options){
      var that = this, type = typeof data === 'function';
      
      if(type){
        options = success
        success = data;
        data = {};
      }

      options = options || {};

      return $.ajax({
        type: options.type || 'post',
        dataType: options.dataType || 'json',
        data: data,
        url: url,
        success: function(res){
          if(res.status === 0) {
            success && success(res);
          } else {
            layer.msg(res.msg || res.code, {shift: 6});
            options.error && options.error();
          }
        }, error: function(e){
          layer.msg('请求异常，请重试', {shift: 6});
          options.error && options.error(e);
        }
      });
    }

    //计算字符长度
    ,charLen: function(val){
      var arr = val.split(''), len = 0;
      for(var i = 0; i <  val.length ; i++){
        arr[i].charCodeAt(0) < 299 ? len++ : len += 2;
      }
      return len;
    }
    
    ,form: {}

    //简易编辑器
    ,layEditor: function(options){
      var html = ['<div class="layui-unselect fly-edit">'
        ,'<span type="face" title="插入表情"><i class="iconfont icon-yxj-expression" style="top: 1px;"></i></span>'
        ,'<span type="picture" title="插入图片：img[src]"><i class="iconfont icon-tupian"></i></span>'
        ,'<span type="href" title="超链接格式：a(href)[text]"><i class="iconfont icon-lianjie"></i></span>'
        ,'<span type="code" title="插入代码或引用"><i class="iconfont icon-emwdaima" style="top: 1px;"></i></span>'
        ,'<span type="hr" title="插入水平线">hr</span>'
        ,'<span type="yulan" title="预览"><i class="iconfont icon-yulan1"></i></span>'
      ,'</div>'].join('');

      var log = {}, mod = {
        face: function(editor, self){ //插入表情
          var str = '', ul, face = fly.faces;
          for(var key in face){
            str += '<li title="'+ key +'"><img src="'+ face[key] +'"></li>';
          }
          str = '<ul id="LAY-editface" class="layui-clear">'+ str +'</ul>';
          layer.tips(str, self, {
            tips: 3
            ,time: 0
            ,skin: 'layui-edit-face'
          });
          $(document).on('click', function(){
            layer.closeAll('tips');
          });
          $('#LAY-editface li').on('click', function(){
            var title = $(this).attr('title') + ' ';
            layui.focusInsert(editor[0], 'face' + title);
          });
        }
        ,picture: function(editor){ //插入图片
          layer.open({
            type: 1
            ,id: 'fly-jie-upload'
            ,title: '插入图片'
            ,area: 'auto'
            ,shade: false
            ,area: '465px'
            ,fixed: false
            ,offset: [
              editor.offset().top - $(window).scrollTop() + 'px'
              ,editor.offset().left + 'px'
            ]
            ,skin: 'layui-layer-border'
            ,content: ['<ul class="layui-form layui-form-pane" style="margin: 20px;">'
              ,'<li class="layui-form-item">'
                ,'<label class="layui-form-label">URL</label>'
                ,'<div class="layui-input-inline">'
                    ,'<input required name="image" placeholder="支持直接粘贴远程图片地址" value="" class="layui-input">'
                  ,'</div>'
                  ,'<button type="button" class="layui-btn layui-btn-primary" id="uploadImg"><i class="layui-icon">&#xe67c;</i>上传图片</button>'
              ,'</li>'
              ,'<li class="layui-form-item" style="text-align: center;">'
                ,'<button type="button" lay-submit lay-filter="uploadImages" class="layui-btn">确认</button>'
              ,'</li>'
            ,'</ul>'].join('')
            ,success: function(layero, index){
              var image =  layero.find('input[name="image"]');

              //执行上传实例
              upload.render({
                elem: '#uploadImg'
                ,url: '/api/upload/'
                ,size: 200
                ,done: function(res){
                  if(res.status == 0){
                    image.val(res.url);
                  } else {
                    layer.msg(res.msg, {icon: 5});
                  }
                }
              });
              
              form.on('submit(uploadImages)', function(data){
                var field = data.field;
                if(!field.image) return image.focus();
                layui.focusInsert(editor[0], 'img['+ field.image + '] ');
                layer.close(index);
              });
            }
          });
        }
        ,href: function(editor){ //超链接
          layer.prompt({
            title: '请输入合法链接'
            ,shade: false
            ,fixed: false
            ,id: 'LAY_flyedit_href'
            ,offset: [
              editor.offset().top - $(window).scrollTop() + 'px'
              ,editor.offset().left + 'px'
            ]
          }, function(val, index, elem){
            if(!/^http(s*):\/\/[\S]/.test(val)){
              layer.tips('这根本不是个链接，不要骗我。', elem, {tips:1})
              return;
            }
            layui.focusInsert(editor[0], ' a('+ val +')['+ val + '] ');
            layer.close(index);
          });
        }
        ,code: function(editor){ //插入代码
          layer.prompt({
            title: '请贴入代码或任意文本'
            ,formType: 2
            ,maxlength: 10000
            ,shade: false
            ,id: 'LAY_flyedit_code'
            ,area: ['800px', '360px']
          }, function(val, index, elem){
            layui.focusInsert(editor[0], '[pre]\n'+ val + '\n[/pre]');
            layer.close(index);
          });
        }
        ,hr: function(editor){ //插入水平分割线
          layui.focusInsert(editor[0], '[hr]');
        }
        ,yulan: function(editor){ //预览
          var content = editor.val();
          
          content = /^\{html\}/.test(content) 
            ? content.replace(/^\{html\}/, '')
          : fly.content(content);

          layer.open({
            type: 1
            ,title: '预览'
            ,shade: false
            ,area: ['100%', '100%']
            ,scrollbar: false
            ,content: '<div class="detail-body" style="margin:20px;">'+ content +'</div>'
          });
        }
      };
      
      layui.use('face', function(face){
        options = options || {};
        fly.faces = face;
        $(options.elem).each(function(index){
          var that = this, othis = $(that), parent = othis.parent();
          parent.prepend(html);
          parent.find('.fly-edit span').on('click', function(event){
            var type = $(this).attr('type');
            mod[type].call(that, othis, this);
            if(type === 'face'){
              event.stopPropagation()
            }
          });
        });
      });
      
    }

    ,escape: function(html){
      return String(html||'').replace(/&(?!#?[a-zA-Z0-9]+;)/g, '&amp;')
      .replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/'/g, '&#39;').replace(/"/g, '&quot;');
    }

    //内容转义
    ,content: function(content){
      //支持的html标签
      var html = function(end){
        return new RegExp('\\n*\\['+ (end||'') +'(pre|hr|div|span|p|table|thead|th|tbody|tr|td|ul|li|ol|li|dl|dt|dd|h2|h3|h4|h5)([\\s\\S]*?)\\]\\n*', 'g');
      };
      content = fly.escape(content||'') //XSS
      .replace(/img\[([^\s]+?)\]/g, function(img){  //转义图片
        return '<img src="' + img.replace(/(^img\[)|(\]$)/g, '') + '">';
      }).replace(/@(\S+)(\s+?|$)/g, '@<a href="javascript:;" class="fly-aite">$1</a>$2') //转义@
      .replace(/face\[([^\s\[\]]+?)\]/g, function(face){  //转义表情
        var alt = face.replace(/^face/g, '');
        return '<img alt="'+ alt +'" title="'+ alt +'" src="' + fly.faces[alt] + '">';
      }).replace(/a\([\s\S]+?\)\[[\s\S]*?\]/g, function(str){ //转义链接
        var href = (str.match(/a\(([\s\S]+?)\)\[/)||[])[1];
        var text = (str.match(/\)\[([\s\S]*?)\]/)||[])[1];
        if(!href) return str;
        var rel =  /^(http(s)*:\/\/)\b(?!(\w+\.)*(sentsin.com|layui.com))\b/.test(href.replace(/\s/g, ''));
        return '<a href="'+ href +'" target="_blank"'+ (rel ? ' rel="nofollow"' : '') +'>'+ (text||href) +'</a>';
      }).replace(html(), '\<$1 $2\>').replace(html('/'), '\</$1\>') //转移HTML代码
      .replace(/\n/g, '<br>') //转义换行   
      return content;
    }
    
    //新消息通知
    /*,newmsg: function(){
      var elemUser = $('.fly-nav-user');
      if(layui.cache.user.uid !== -1 && elemUser[0]){
        fly.json('/message/nums/', {
          _: new Date().getTime()
        }, function(res){
          if(res.status === 0 && res.count > 0){
            var msg = $('<a class="fly-nav-msg" href="javascript:;">'+ res.count +'</a>');
            elemUser.append(msg);
            msg.on('click', function(){
              fly.json('/message/read', {}, function(res){
                if(res.status === 0){
                  location.href = '/user/message/';
                }
              });
            });
            layer.tips('你有 '+ res.count +' 条未读消息', msg, {
              tips: 3
              ,tipsMore: true
              ,fixed: true
            });
            msg.on('mouseenter', function(){
              layer.closeAll('tips');
            })
          }
        });
      }
      return arguments.callee;
    }*/
    
  };

  //签到
  var tplSignin = ['{{# if(d.signed){ }}'
    ,'<button class="layui-btn layui-btn-disabled">今日已签到</button>'
    ,'<span>获得了<cite>{{ d.experience }}</cite>飞吻</span>'
  ,'{{# } else { }}'
    ,'<button class="layui-btn layui-btn-danger" id="LAY_signin">今日签到</button>'
    ,'<span>可获得<cite>{{ d.experience }}</cite>飞吻</span>'
  ,'{{# } }}'].join('')
  ,tplSigninDay = '已连续签到<cite>{{ d.days }}</cite>天'

  ,signRender = function(data){
    laytpl(tplSignin).render(data, function(html){
      elemSigninMain.html(html);
    });
    laytpl(tplSigninDay).render(data, function(html){
      elemSigninDays.html(html);
    });
  }

  ,elemSigninHelp = $('#LAY_signinHelp')
  ,elemSigninTop = $('#LAY_signinTop')
  ,elemSigninMain = $('.fly-signin-main')
  ,elemSigninDays = $('.fly-signin-days');
  
  if(elemSigninMain[0]){
    /*
    fly.json('/sign/status', function(res){
      if(!res.data) return;
      signRender.token = res.data.token;
      signRender(res.data);
    });
    */
  }
  $('body').on('click', '#LAY_signin', function(){
    var othis = $(this);
    if(othis.hasClass(DISABLED)) return;

    fly.json('/sign/in', {
      token: signRender.token || 1
    }, function(res){
      signRender(res.data);
    }, {
      error: function(){
        othis.removeClass(DISABLED);
      }
    });

    othis.addClass(DISABLED);
  });

  //签到说明
  elemSigninHelp.on('click', function(){
    layer.open({
      type: 1
      ,title: '签到说明'
      ,area: '300px'
      ,shade: 0.8
      ,shadeClose: true
      ,content: ['<div class="layui-text" style="padding: 20px;">'
        ,'<blockquote class="layui-elem-quote">“签到”可获得社区飞吻，规则如下</blockquote>'
        ,'<table class="layui-table">'
          ,'<thead>'
            ,'<tr><th>连续签到天数</th><th>每天可获飞吻</th></tr>'
          ,'</thead>'
          ,'<tbody>'
            ,'<tr><td>＜5</td><td>5</td></tr>'
            ,'<tr><td>≥5</td><td>10</td></tr>'
            ,'<tr><td>≥15</td><td>15</td></tr>'
            ,'<tr><td>≥30</td><td>20</td></tr>'
          ,'</tbody>'
        ,'</table>'
        ,'<ul>'
          ,'<li>中间若有间隔，则连续天数重新计算</li>'
          ,'<li style="color: #FF5722;">不可利用程序自动签到，否则飞吻清零</li>'
        ,'</ul>'
      ,'</div>'].join('')
    });
  });

  //签到活跃榜
  var tplSigninTop = ['{{# layui.each(d.data, function(index, item){ }}'
    ,'<li>'
      ,'<a href="/u/{{item.uid}}" target="_blank">'
        ,'<img src="{{item.user.avatar}}">'
        ,'<cite class="fly-link">{{item.user.username}}</cite>'
      ,'</a>'
      ,'{{# var date = new Date(item.time); if(d.index < 2){ }}'
        ,'<span class="fly-grey">签到于 {{ layui.laytpl.digit(date.getHours()) + ":" + layui.laytpl.digit(date.getMinutes()) + ":" + layui.laytpl.digit(date.getSeconds()) }}</span>'
      ,'{{# } else { }}'
        ,'<span class="fly-grey">已连续签到 <i>{{ item.days }}</i> 天</span>'
      ,'{{# } }}'
    ,'</li>'
  ,'{{# }); }}'
  ,'{{# if(d.data.length === 0) { }}'
    ,'{{# if(d.index < 2) { }}'
      ,'<li class="fly-none fly-grey">今天还没有人签到</li>'
    ,'{{# } else { }}'
      ,'<li class="fly-none fly-grey">还没有签到记录</li>'
    ,'{{# } }}'
  ,'{{# } }}'].join('');

  elemSigninTop.on('click', function(){
    var loadIndex = layer.load(1, {shade: 0.8});
    fly.json('../json/signin.js', function(res){ //实际使用，请将 url 改为真实接口
      var tpl = $(['<div class="layui-tab layui-tab-brief" style="margin: 5px 0 0;">'
        ,'<ul class="layui-tab-title">'
          ,'<li class="layui-this">最新签到</li>'
          ,'<li>今日最快</li>'
          ,'<li>总签到榜</li>'
        ,'</ul>'
        ,'<div class="layui-tab-content fly-signin-list" id="LAY_signin_list">'
          ,'<ul class="layui-tab-item layui-show"></ul>'
          ,'<ul class="layui-tab-item">2</ul>'
          ,'<ul class="layui-tab-item">3</ul>'
        ,'</div>'
      ,'</div>'].join(''))
      ,signinItems = tpl.find('.layui-tab-item');

      layer.close(loadIndex);

      layui.each(signinItems, function(index, item){
        var html = laytpl(tplSigninTop).render({
          data: res.data[index]
          ,index: index
        });
        $(item).html(html);
      });

      layer.open({
        type: 1
        ,title: '签到活跃榜 - TOP 20'
        ,area: '300px'
        ,shade: 0.8
        ,shadeClose: true
        ,id: 'layer-pop-signintop'
        ,content: tpl.prop('outerHTML')
      });

    }, {type: 'get'});
  });


  //回帖榜
  var tplReply = ['{{# layui.each(d.data, function(index, item){ }}'
    ,'<dd>'
      ,'<a href="/u/{{item.uid}}">'
        ,'<img src="{{item.user.avatar}}">'
        ,'<cite>{{item.user.username}}</cite>'
        ,'<i>{{item["count(*)"]}}次回答</i>'
      ,'</a>'
    ,'</dd>'
  ,'{{# }); }}'].join('')
  ,elemReply = $('#LAY_replyRank');

  if(elemReply[0]){
    /*
    fly.json('/top/reply/', {
      limit: 20
    }, function(res){
      var html = laytpl(tplReply).render(res);
      elemReply.find('dl').html(html);
    });
    */
  };

  //相册
  if($(window).width() > 750){
    layer.photos({
      photos: '.photos'
      ,zIndex: 9999999999
      ,anim: -1
    });
  } else {
    $('body').on('click', '.photos img', function(){
      window.open(this.src);
    });
  }


  //搜索
  $('.fly-search').on('click', function(){
    layer.open({
      type: 1
      ,title: false
      ,closeBtn: false
      //,shade: [0.1, '#fff']
      ,shadeClose: true
      ,maxWidth: 10000
      ,skin: 'fly-layer-search'
      ,content: ['<form action="http://cn.bing.com/search">'
        ,'<input autocomplete="off" placeholder="搜索内容，回车跳转" type="text" name="q">'
      ,'</form>'].join('')
      ,success: function(layero){
        var input = layero.find('input');
        input.focus();

        layero.find('form').submit(function(){
          var val = input.val();
          if(val.replace(/\s/g, '') === ''){
            return false;
          }
          input.val('site:layui.com '+ input.val());
      });
      }
    })
  });


  //发送激活邮件
  fly.activate = function(email){
    fly.json('/api/activate/', {}, function(res){
      if(res.status === 0){
        layer.alert('已成功将激活链接发送到了您的邮箱，接受可能会稍有延迟，请注意查收。', {
          icon: 1
        });
      };
    });
  };
  $('#LAY-activate').on('click', function(){
    fly.activate($(this).attr('email'));
  });

  //点击@
  $('body').on('click', '.fly-aite', function(){
    var othis = $(this), text = othis.text();
    if(othis.attr('href') !== 'javascript:;'){
      return;
    }
    text = text.replace(/^@|（[\s\S]+?）/g, '');
    othis.attr({
      href: '/jump?username='+ text
      ,target: '_blank'
    });
  });

  //根据ip获取城市
  if($('#L_city').val() === ''){
    $.getScript('http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=js', function(){
      $('#L_city').val(remote_ip_info.country+""+remote_ip_info.province+""+remote_ip_info.city||'');
    });
  }

    //上传头像图片
    if($('.upload-img')[0]){
      layui.use('upload', function(upload){
        var avatarAdd = $('.avatar-add');
        var userid = $('#hiddenUser').val();
        upload.render({
          elem: '.upload-img'
          ,url: 'uploadtouxiang.action'
          ,size: 200
          ,data: {id:userid} 
          ,before: function(obj){
            obj.preview(function(index, file, result){
                  $('#touxiangimg').attr('src', result); //图片链接（base64）
              });
          }
          ,done: function(res){
            var height = (window.screen.height)/2;
            if(result.statusCode == 200){
            layer.msg(result.message,{icon:6,offset:height});
          }else if(result.statusCode == 300){
            layer.msg(result.message,{icon:5,offset:height});
          }
          }
          ,error: function(){
            var height = (window.screen.height)/2;
            layer.msg('接口请求异常',{icon:0,offset:height});
          }
        });
      });
    }

  //表单提交
  form.on('submit(*)', function(data){
    var action = $(data.form).attr('action'), button = $(data.elem);
    fly.json(action, data.field, function(res){
      var end = function(){
        if(res.action){
          location.href = res.action;
        } else {
          fly.form[action||button.attr('key')](data.field, data.form);
        }
      };
      if(res.status == 0){
        button.attr('alert') ? layer.alert(res.msg, {
          icon: 1,
          time: 10*1000,
          end: end
        }) : end();
      };
    });
    return false;
  });

  //加载特定模块
/*  if(layui.cache.page && layui.cache.page !== 'index'){
    var extend = {};
    extend[layui.cache.page] = layui.cache.page;
    layui.extend(extend);
    layui.use(layui.cache.page);
  }*/
  
  //加载IM
  if(!device.android && !device.ios){
    //layui.use('im');
  }


  //banner
  carousel.render({
    elem: '#banner'
    ,width: '100%'
    ,height: '280px'
    ,interval: 5000
  });

  //加载编辑器
  fly.layEditor({
    elem: '.fly-editor'
  });

  //手机设备的简单适配
  var treeMobile = $('.site-tree-mobile')
  ,shadeMobile = $('.site-mobile-shade')

  treeMobile.on('click', function(){
    $('body').addClass('site-mobile');
  });

  shadeMobile.on('click', function(){
    $('body').removeClass('site-mobile');
  });

  //获取统计数据
  $('.fly-handles').each(function(){
    var othis = $(this);
    $.get('/api/handle?alias='+ othis.data('alias'), function(res){
      othis.html('（下载量：'+ res.number +'）');
    })
  });
  
  //固定Bar
  util.fixbar({
    bgcolor: '#009688'
  });

  
  $(function(){

      //时钟
      $('#blog-date').html(new Date().toLocaleString());
      setInterval(function() {
      	$('#blog-date').html(new Date().toLocaleString());
      }, 1000);
      //左侧菜单显示隐藏
      var leftmenusswitch = $('.leftmenusswitch');
      var dynamic_navigation = $('.dynamic-navigation');
      
      leftmenusswitch.on('click',function(){
        var showleftmenu = sessionStorage.getItem("showmenu");
        if(showleftmenu ==null || showleftmenu ===''){
          dynamic_navigation.animate({left:'0px',opacity: "show"});
          leftmenusswitch.find('i').hide();
          sessionStorage.setItem("showmenu","show");
        };
        if(showleftmenu === 'show'){
          
          dynamic_navigation.animate({left:'-200px'});
          leftmenusswitch.find('i').show();
          sessionStorage.setItem("showmenu","");
        }
      });
      
      //格言
      getMotto();
      setInterval(function(){
        getMotto();
      },10000);
      
      //相册背景音乐
      setTimeout(function(){
        var albumaudio = $('#albumaudio').attr("src","../../res/others/mplayer/radio/1.mp3");
      },1000);
      
  
    //响应式处理
    var currentWidth = document.documentElement.clientWidth;
    if(currentWidth < 768){
      //搜索框响应式
      $('.top3-box .inp').css('width','252px');
      $('.top3-box .inp table .cons1').css('width','200px');
      $('.top3-box .inp table .cons1 input').css('width','150px');
      //音乐播放器
      //$('.mp').css('width','320px');
      //音乐故事响应式
      $('.musicstoryfield').css('width','320px');
      //个人模块
      var w = (currentWidth -200)/2;
      $('.defaultpersion>.persionresume').css('left',w+'px');
    }


    //页面右侧相关列表徽章颜色控制
    $('.badge-list dd:nth-child(10n-6)').find('.layui-badge').removeClass('layui-bg-gray').addClass('layui-bg-orange');
    $('.badge-list dd:nth-child(10n-7)').find('.layui-badge').removeClass('layui-bg-gray').addClass('layui-bg-green');
    });

  //获取格言
  function getMotto(){
    var motto = $('.motto');
      //服务器环境下请求ajax
      // $.ajax({
      //   url:'/blog1.0/res/others/motto.json',
      //   type:'GET',
      //   dataType: "json",
      //   success:function(data){
      //     var random = Math.floor(Math.random()*55);
      //     motto.html(data[random]);
      //   }
      // });
      
      //静态页面
      var data = [
        "真正的才智是刚毅的志向。",
        "人的理想志向往往和他的能力成正比。",
        "在强者的眼中，没有最好，只有更好。",
        "盆景秀木正因为被人溺爱，才破灭了成为栋梁之材的梦。",
        "永远都不要放弃自己，勇往直前，直至成功！",
        "萤火虫的光点虽然微弱，但亮着便是向黑暗挑战。",
        "想而奋进的过程，其意义远大于未知的结果。",
        "努力向上的开拓，才使弯曲的竹鞭化作了笔直的毛竹。",
        "生命力的意义在于拼搏，因为世界本身就是一个竞技场。",
        "通过云端的道路，只亲吻攀登者的足迹。",
        "不经巨大的困难，不会有伟大的事业。",
        "泉水，奋斗之路越曲折，心灵越纯洁。",
        "人的一生，可以有所作为的时机只有一次，那就是现在。",
        "时间顺流而下，生活逆水行舟。",
        "生命的道路上永远没有捷径可言，只有脚踏实地走下去。",
        "一个人，只要知道付出爱与关心，她内心自然会被爱与关心充满。",
        "有大快乐的人，必有大哀痛；有大成功的人，必有大孤独。",
        "成功等于目标，其他都是这句话的注解。",
        "路在自己脚下，没有人可以决定我的方向。",
        "命运是不存在的，它不过是失败者拿来逃避现实的借口。",
        "生命太过短暂，今天放弃了明天不一定能得到。",
        "沉湎于希望的人和守株待兔的樵夫没有什么两样。",
        "每一发奋努力的背后，必有加倍的赏赐。",
        "能克服困难的人，可使困难化为良机。",
        "美丽的蓝图，落在懒汉手里，也不过是一页废纸。",
        "一时的挫折往往可以通过不屈的搏击，变成学问及见识。",
        "没有创造的生活不能算生活，只能算活着。",
        "只要还有明天，今天就永远是起跑线。",
        "如果命运不宠你，请你别伤害自己。",
        "趁年轻去努力，别对不起你儿时吹的牛逼。",
        "没有人能一路单纯到底，但要记住，别忘了最初的自己。",
        "胜利属于坚持到最后的人。",
        "经过大海的一番磨砺，卵石才变得更加美丽光滑。",
        "河流之所以能够到达目的地，是因为它懂得怎样避开障碍。",
        "不可压倒一切，但你也不能被一切压倒。",
        "一个人的成败，与他的心量有很大关系。",
        "你失去了金钱，可以再挣；你失去了一生，便再也不能回头。",
        "生命的多少用时间计算，生命的价值用贡献计算。",
        "贝壳虽然死了，却把它的美丽留给了整个世界。",
        "路靠自己走，就算再坎坷，也要自己过。",
        "只有承担起旅途风雨，才能最终守得住彩虹满天。",
        "没有一种不通过蔑视、忍受和奋斗就可以征服的命运。",
        "不管现在有多么艰辛，我们也要做个生活的舞者。",
        "命运从来不会同情弱者。",
        "不怕万人阻挡在前方，只怕自己先行投降。",
        "生活其实很简单，过了今天就是明天。",
        "路的尽头，仍然是路，只要你愿意走。",
        "现在不努力，将来拿什么向曾经抛弃你的人证明它有多瞎。",
        "尽力做好一件事，实乃人生之首务。",
        "应该让别人的生活因为有了你的生存而更加美好。",
        "快乐是一种香水，无法倒在别人身上，而自己却不沾上一些。",
        "你配不上自己的野心，也辜负了曾经历的苦难。",
        "人生没有如果，只有后果和结果。少问别人为什么，多问自己凭什么。",
        "没有人能替你承受痛苦，也没有人能抢走你的坚强。",
        "无论你觉得自己多么的不幸，永远有人比你更加不幸。"
    ]
      var random = Math.floor(Math.random()*55);
      motto.html(data[random]);
  }

   //搜索框
   $('.cons2').mouseover(function(){
    $('.sss').css('color','rgb(255,255,255)');
    $('.cons2').css('border','1px solid rgb(255, 103, 0)');
  });
  $('.cons2').mouseleave(function(){
    $('.sss').css('color','#616161');
    $('.cons2').css('border','1px solid #E0E0E0');
  });
  $('.inp').mouseenter(function(){
    $('.cons1').css('border','1px solid rgb(176, 176, 176)');
    $('.cons2').css('border','1px solid rgb(176, 176, 176)');
  });
  $('.inp').mouseleave(function(){
    if($(this).attr('flag') === '1'){
      $('.cons1').css('border','1px solid rgb(255, 103, 0)');
      $('.cons2').css('border','1px solid rgb(255, 103, 0)');
    }
    if($(this).attr('flag') === '0'){
      $('.cons2').css('border','1px solid #E0E0E0');
      $('.cons1').css('border','1px solid #E0E0E0');
        
    }

  });

  $('.inpu').click(function(){
    $('.inp').attr('flag',1);
    //	console.log("inp----flag"+$('.inp').attr('flag'));
    $(this).siblings().fadeOut();
    $('.cons1').css('border','1px solid rgb(255, 103, 0)');
    $('.cons2').css('border','1px solid rgb(255, 103, 0)');
  });

  $(document).ready(function() {

      $('.inpu').blur(function(){
      $('.inp').attr('flag',0);
      var str = $('.inpu').val();
      //console.log(str);
      if(!str){
        $(this).siblings().fadeIn();
        $('.cons1').css('border','1px solid #E0E0E0');
          $('.cons2').css('border','1px solid #E0E0E0');
      }else{
        $('.cons1').css('border','1px solid rgb(255, 103, 0)');
        $('.cons2').css('border','1px solid rgb(255, 103, 0)');
      }
    
    });
  });
  
  //监听页面刷新
  window.onunload = function() {
    var leftmenusswitch = $('.leftmenusswitch');
    sessionStorage.setItem("showmenu","");
    leftmenusswitch.find('i').show();
   };
   //监听页面大小
   window.onresize = function(){
    var currentWidth = document.documentElement.clientWidth;
    if(currentWidth > 768){
      //隐藏菜单监听
      var dynamic_navigation = $('.dynamic-navigation');
      var leftmenusswitch = $('.leftmenusswitch');
      dynamic_navigation.animate({left:'-200px'});
      leftmenusswitch.find('i').show();
      sessionStorage.setItem("showmenu","");

      //响应式监听
      //搜索框
      $('.top3-box .inp').css('width','500px');
      $('.top3-box .inp table .cons1').css('width','448px');
      $('.top3-box .inp table .cons1 input').css('width','420px');
      
      //音乐故事响应式
      //$('.musicstoryfield').css('width','550px');
      //个人模块
      $('.defaultpersion>.persionresume').css('left','92px');
     }
     //响应式监听
     if(currentWidth < 768){
       //搜索框
      $('.top3-box .inp').css('width','252px');
      $('.top3-box .inp table .cons1').css('width','200px');
      $('.top3-box .inp table .cons1 input').css('width','150px');
     
      //音乐故事响应式
      //$('.musicstoryfield').css('width','320px');
      //个人模块
      var w = (currentWidth -200)/2;
      $('.defaultpersion>.persionresume').css('left',w+'px')
    }
   }

   //监听页面点击事件
   document.onmousedown = function(event){
    var showleftmenu = sessionStorage.getItem("showmenu");
    var leftmenusswitch = $('.leftmenusswitch');
    var dynamic_navigation = $('.dynamic-navigation');
   
    
    if(showleftmenu ==='show'){
      dynamic_navigation.animate({left:'-200px'});
      leftmenusswitch.find('i').show();
      sessionStorage.setItem("showmenu","");
    }
   }

   //监听邮箱input change事件
   $('#L_email').change(function() { 
      var  val= $('#L_email').val();
      layer.tips(val+'', '#L_email',{tips:[1,'#33ABA0'],time:2000});
    });
  

  exports('fly', fly);

});

