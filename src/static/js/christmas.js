//底層共用
var iBase = {
Id: function(name){
	return document.getElementById(name);
},
//設置元素透明度,透明度值按IE規則計,即0~100
SetOpacity: function(ev, v){
	ev.filters ? ev.style.filter = 'alpha(opacity=' + v + ')' : ev.style.opacity = v / 100;
	}
}
//淡入效果(含淡入到指定透明度)
function fadeIn(elem, speed, opacity){
	/*
	 * 參數說明
	 * elem==>需要淡入的元素
	 * speed==>淡入速度,正整數(可選)
	 * opacity==>淡入到指定的透明度,0~100(可選)
	 */
	speed = speed || 20;
	opacity = opacity || 100;
	//顯示元素,並將元素值為0透明度(不可見)
	elem.style.display = 'block';
	iBase.SetOpacity(elem, 0);
	//初始化透明度變化值為0
	var val = 0;
	//循環將透明值以5遞增,即淡入效果
	(function(){
		iBase.SetOpacity(elem, val);
		val += 5;
		if (val <= opacity) {
			setTimeout(arguments.callee, speed)
		}
	})();
}
//淡出效果(含淡出到指定透明度)
function fadeOut(elem, speed, opacity){
	/*
	 * 參數說明
	 * elem==>需要淡入的元素
	 * speed==>淡入速度,正整數(可選)
	 * opacity==>淡入到指定的透明度,0~100(可選)
	 */
	speed = speed || 20;
	opacity = opacity || 0;
	//初始化透明度變化值為0
	var val = 100;
	//循環將透明值以10遞減,即淡出效果
	(function(){
		iBase.SetOpacity(elem, val);
		val -= 10;
		if (val >= opacity) {
			setTimeout(arguments.callee, speed);
		}else if (val < 0) {
			//元素透明度為0後隱藏元素
			elem.style.display = 'none';
		}
	})();
}
function DispMagicEmot(MagicID,H,W){
	fadeIn(document.getElementById('MagicFace'), 20, 100);
	MagicFaceUrl = "/christmas/";
	document.getElementById("MagicFace").innerHTML = '<iframe width="'+W+'" height="'+H+'" allowtransparency="true" seamless="seamless" frameborder="0" src="'+MagicFaceUrl+'" style="position: fixed;"></iframe>';
	//document.getElementById("MagicFace").style.top = (document.body.scrollTop+((document.body.clientHeight-300)/2))+"px";
	//document.getElementById("MagicFace").style.left = (document.body.scrollLeft+((document.body.clientWidth-480)/2))+"px";
	//document.getElementById("MagicFace").style.top = (window.screen.availHeight-300)/2+"px";
	//document.getElementById("MagicFace").style.left = (window.screen.availWidth-480)/2+"px"; 
	document.getElementById("MagicFace").style.bottom = (H+50)+"px";
	document.getElementById("MagicFace").style.right = (W-50)+"px"; 
	document.getElementById("MagicFace").style.visibility = 'visible';
	MagicID += Math.random();
	setTimeout(fadeOut(document.getElementById('MagicFace'), 1000, 0), 10000);
	NowMeID = MagicID;
}
DispMagicEmot(144,370,500);