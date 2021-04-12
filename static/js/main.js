//for sha1()
function encodeUTF8(s) {
  var i, r = [], c, x;
  for (i = 0; i < s.length; i++)
    if ((c = s.charCodeAt(i)) < 0x80) r.push(c);
    else if (c < 0x800) r.push(0xC0 + (c >> 6 & 0x1F), 0x80 + (c & 0x3F));
    else {
      if ((x = c ^ 0xD800) >> 10 == 0) //对四字节UTF-16转换为Unicode
        c = (x << 10) + (s.charCodeAt(++i) ^ 0xDC00) + 0x10000,
          r.push(0xF0 + (c >> 18 & 0x7), 0x80 + (c >> 12 & 0x3F));
      else r.push(0xE0 + (c >> 12 & 0xF));
      r.push(0x80 + (c >> 6 & 0x3F), 0x80 + (c & 0x3F));
    };
  return r;
}
// 字符串加密成 hex 字符串
function sha1(s) {
  var data = new Uint8Array(encodeUTF8(s))
  var i, j, t;
  var l = ((data.length + 8) >>> 6 << 4) + 16, s = new Uint8Array(l << 2);
  s.set(new Uint8Array(data.buffer)), s = new Uint32Array(s.buffer);
  for (t = new DataView(s.buffer), i = 0; i < l; i++)s[i] = t.getUint32(i << 2);
  s[data.length >> 2] |= 0x80 << (24 - (data.length & 3) * 8);
  s[l - 1] = data.length << 3;
  var w = [], f = [
    function () { return m[1] & m[2] | ~m[1] & m[3]; },
    function () { return m[1] ^ m[2] ^ m[3]; },
    function () { return m[1] & m[2] | m[1] & m[3] | m[2] & m[3]; },
    function () { return m[1] ^ m[2] ^ m[3]; }
  ], rol = function (n, c) { return n << c | n >>> (32 - c); },
    k = [1518500249, 1859775393, -1894007588, -899497514],
    m = [1732584193, -271733879, null, null, -1009589776];
  m[2] = ~m[0], m[3] = ~m[1];
  for (i = 0; i < s.length; i += 16) {
    var o = m.slice(0);
    for (j = 0; j < 80; j++)
      w[j] = j < 16 ? s[i + j] : rol(w[j - 3] ^ w[j - 8] ^ w[j - 14] ^ w[j - 16], 1),
        t = rol(m[0], 5) + f[j / 20 | 0]() + m[4] + w[j] + k[j / 20 | 0] | 0,
        m[1] = rol(m[1], 30), m.pop(), m.unshift(t);
    for (j = 0; j < 5; j++)m[j] = m[j] + o[j] | 0;
  };
  t = new DataView(new Uint32Array(m).buffer);
  for (var i = 0; i < 5; i++)m[i] = t.getUint32(i << 2);

  var hex = Array.prototype.map.call(new Uint8Array(new Uint32Array(m).buffer), function (e) {
    return (e < 16 ? "0" : "") + e.toString(16);
  }).join("");
  return hex;
}





/*封装的ajax函数
* v0.1 https://www.cnblogs.com/wang-zhang/p/9883654.html
* v0.2 添加了json类型自动转换
*/
function ajax(options){
    //创建一个ajax对象
    var xhr = new XMLHttpRequest() || new ActiveXObject("Microsoft,XMLHTTP");
    //数据的处理 {a:1,b:2} a=1&b=2;
    var str = "";
    for(var key in options.data){
        str+="&"+key+"="+options.data[key];
    }
    str = str.slice(1)
    if(options.method == "get"){
        var url = options.url+"?"+str;
        xhr.open("get",url);
        xhr.send();
    }else if(options.method == "post"){
        xhr.open("post",options.url);
        xhr.setRequestHeader("content-type","application/x-www-form-urlencoded");
        xhr.send(str)
    }
    //监听
    xhr.onreadystatechange = function(){
        //当请求成功的时候
        if(xhr.readyState == 4 && xhr.status == 200){
            var text = xhr.responseText;
			if(options.type=="json"){
				text=JSON.parse(text);
			}
            //将请求的数据传递给成功回调函数
            options.success&&options.success(text)
        }else if(xhr.status != 200){
            //当失败的时候将服务器的状态传递给失败的回调函数
            options.error&&options.error(xhr.status);
        }
    }
}
/*
ajax({
    method:"get/post",
    url:"请求的地址",
    data:{},
    success:function(text){
        console.log(text)
    },
	error: function(num){
		//
	},
	type: "json/text"
})
*/











var oTable=document.getElementsByTagName("table")[0];
var aTrH=oTable.getElementsByClassName("header");//需要保留
var aTrD=oTable.getElementsByClassName("dir");//dir
var aTrF=oTable.getElementsByClassName("file");//file
var order=-1; //order: desc or asc

var oBtnOrder=document.getElementById("order");
var oBtnDelete=document.getElementById("delete");

var oBtnSubmit=document.getElementById("submit");

//to real array;
aTrF=Array.prototype.slice.call(aTrF)
aTrD=Array.prototype.slice.call(aTrD)

//sort array
function sortByTime(arr, order=1){
	//console.log("sortByTime");
	arr.sort(function(a,b){
		return -( b.getAttribute("data-time") - a.getAttribute("data-time") )*order;
	});
}


//
window.onload=function(){
    var fpath=document.getElementById("fpath").innerHTML;
    document.forms[0].getElementsByTagName('input')[1].value=fpath;
    //console.log("ok")
	
	//排序键
	oBtnOrder.onclick=function(){
		//1.排序
		sortByTime(aTrD, order);
		sortByTime(aTrF, order);
		order=-1*order;//翻转顺序

		//2.插入到虚拟数组中
		var arr=[];
		Array.prototype.push.apply(arr,aTrH)
		Array.prototype.push.apply(arr,aTrF)
		Array.prototype.push.apply(arr,aTrD)

		//3.插入dom
		oTable.innerHTML="";//清空
		for(var i=0;i<arr.length;i++){
			oTable.append(arr[i]);
		}
	}
	oBtnOrder.onclick(); //载入后就排序，最新的在最上层
	
	
	//删除键
	oBtnDelete.onclick=function(){
		var aCheck=document.querySelectorAll("input[type=checkbox]");
		var arr=[];
		for(var i=0;i<aCheck.length;i++){
			if(aCheck[i].checked==true ){
				var url=aCheck[i].parentElement.nextElementSibling.childNodes[2].href;//.replace("/download?","/delete?");
				if(url.search(/fpath/)==-1){
					var fnames=url.match(/filename=(.*?)\&/)[1];
					arr.push(fnames);			
					//console.log(url)
				}
			}
		}
		//
		var error="Possible Errors: 1.必须勾选至少一项;2.暂时不能删除文件夹;";
		if(arr.length==0){
			alert(error);
			return false;
		}
		filenames=arr.join(",");
		// 获取参数，path， filenames
		
		//删除前二次确认
		if(!confirm('确定要删除这些文件吗？('+filenames+')\n此操作可能不可恢复！')) {
			return false;
		}
		
		//ajax向后台发送删除请求
		ajax({
			method:"post",
			url:"/delete",
			data:{'path':fpath, 'filenames':filenames},
			success:function(text){
				//var text=JSON.parse(text);
				alert(text.msg + "\n" +text.filename)
				//console.log("success: ", text)
				document.location.href=document.location.href;
			},
			error: function(num){
				console.log("error: ", num)
			},
			type:"json"
		})

		return false;
	}
	
	
	//单击提交表单时，验证身份
	oBtnForm.onsubmit=function(ev){
		var pass=prompt("请输入上传验证码:", "提示: 大实验室房间号，3个数字") //取消则返回null
		if( pass != null && sha1(pass)=='40bd001563085fc35165329ea1ff5c5ecbdbbeef'){
			return true;
		}else{
			alert("密码错误!")
			ev.preventDefault();  
			return false;
		}
	}
}

