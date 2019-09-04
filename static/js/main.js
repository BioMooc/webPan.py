var oTable=document.getElementsByTagName("table")[0];
var aTrH=oTable.getElementsByClassName("header");//需要保留
var aTrD=oTable.getElementsByClassName("dir");//dir
var aTrF=oTable.getElementsByClassName("file");//file
var order=-1; //order: desc or asc

var oBtn=document.getElementById("order");

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
	
	oBtn.onclick=function(){
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
}