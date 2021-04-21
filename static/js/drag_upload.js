// 拖拽上传 依赖 webPan.css 的样式 .fileBox .fileBoxEnter

//1. 阻止浏览器默认行为
document.addEventListener( "dragleave", function(e) {
     e.preventDefault();
}, false);
document.addEventListener( "drop", function(e) {
     e.preventDefault();
}, false);
document.addEventListener( "dragenter", function(e) {
     e.preventDefault();
}, false);
document.addEventListener( "dragover", function(e) {
     e.preventDefault();
}, false);


//2. 处理拖拽
var dropHandler=function (e) {
    var fileList = e.dataTransfer.files; //获取文件对象
	//其实只支持一个文件拖拽上传
    if (fileList.length != 1) {
		alert('一次只能拖拽上传一个文件！')
        return false;
    }

	// put droped file to input file
	// https://stackoverflow.com/questions/8006715/drag-drop-files-into-standard-html-file-input
	document.getElementById("file").files = e.dataTransfer.files;
}

//3. 设置drop区域: 当文件拖放到drop区域时，就能触发上传。
var oDragWrap = document.getElementById("file"); //drop区域的DOM元素
oDragWrap.addEventListener("drop", function(e){dropHandler(e)} , false);

//进入 高亮显示边框
oDragWrap.addEventListener( "dragenter", function(e){
	var classVal = this.getAttribute("class");
	classVal = classVal.concat(" fileBoxEnter");
	this.setAttribute("class",classVal );
}, false);

// drop 恢复颜色
oDragWrap.addEventListener( "drop", function(e){
	var classVal = this.getAttribute("class");
	classVal = classVal.replace("fileBoxEnter","");
	this.setAttribute("class",classVal );
}, false);
