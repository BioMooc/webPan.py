# 网盘 webPan.py
目的： 用于局域网内文件短暂共享，可以不用U盘了。

## v0.3.5
![screenShot0.3.5](./static/images/webPan_py_v0.3.5.png)

## v0.1.6
![screenShot0.1.6](./static/images/webPan_py.png)




# 环境
- depend: Python3 flask
- test OS: win10, Ubuntu 1804
- version: 0.2
```
C:\Users\admin>flask --version
Flask 1.0.2
Python 3.6.4 (v3.6.4:d48eceb, Dec 19 2017, 06:54:40) [MSC v.1900 64 bit (AMD64)]

$ flask --version
Flask 1.0.2
Python 3.6.8 (default, Aug 20 2019, 17:12:48) 
[GCC 8.3.0]
```




# 现有功能
- 在webPanLib.py中定义根目录
- 浏览和下载文件
- 上传文件
- 删除一个或多个文件到回收站/dustbin/，在 dustbin/ 删除则彻底删除;
- 支持跨域请求静态文件，API是 /file/xx.mp3
	已经添加外链，并图标显示，可右击复制外链。
	例如，网盘显示为 audio/xx.mp3的文件，可以外网访问 init('http://y.biomooc.com:8000/file/audio/xx.mp3')
- 支持在线预览pdf/jpg/png/svg/mp3/mp4/html/txt
- 不同文件类型对应不同的icon图标
- 上传文件需要输入验证码，main.js中设定，默认是 213
- 支持拖拽上传文件




# todo
- 新建文件夹
- 加入多用户功能，文件能设置私有、公开(需要使用数据库)、按口令公开





# 运行方式 How to run
1. 下载项目 $ git clone https://github.com/DawnEve/webPan.py.git
2. 设置 
 - 安装python3的包 $ pip install flask
 - 如果提示缺少其他包，继续安装缺少的包，比如 $ pip install pkgName
 - webPanLib.py中的rootPath为保存文件的路径(有默认值，但是不一定存在，需要用户核实；如果不可写，则无法上传文件);
 - 修改index.py最后一行为合适的ip和端口号(有默认值，但是端口号不一定可用);
3. 进入目录，运行 $ python index.py  #会提示url
4. 在浏览器打开url。
5. 单击文件下载
	- 单击后面的预览图标可以预览
	- 右击后面的外链，选择复制链接，该链接支持外链，然后到其他web应用中使用该网络资源。
6. 上传密码的设置，在js/main.js的 oBtnForm.onsubmit 中。






# 项目文件结构
```
|-- index.py 入口文件
|-- webPanLib.py 定义函数和常量
|-- static/
    |--css/
        |--webPan.css
    |--js/
        |--main.js
    |--images/
|-- ReadMe.txt 说明文档
|-- dustbin/ 回收站
```

