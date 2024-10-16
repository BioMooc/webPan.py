# 网盘 webPan.py
目的： 用于局域网内文件短暂共享，可以不用U盘了。

## v0.3.5
![screenShot0.3.5](./static/images/webPan_py_v0.3.5.png)

## v0.1.6
![screenShot0.1.6](./static/images/webPan_py.png)




# 环境
- depend: Python3 flask
- test OS: win11, Ubuntu 2204, CentOS7.9
- version: 0.7.1
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
- 浏览和下载文件
- 上传文件
- 删除一个或多个文件到回收站/dustbin/，在 dustbin/ 删除则彻底删除;
- 支持跨域请求静态文件，API是 /file/xx.mp3
	* 已支持外链，右击文件名后的小图标，复制外链
	* 例如，网盘显示为 audio/xx.mp3的文件，可以外网访问 init('http://j3.biomooc.com:8000/file/audio/xx.mp3')
- 支持在线预览pdf/jpg/png/svg/mp3/mp4/html/txt
- 不同文件类型对应不同的icon图标
- 上传文件需要输入验证码，main.js中设定，默认是 213
- 支持拖拽上传文件 [v0.3.8]
- 预览代码 [v0.5.7]
- 预览 jupyter notebook: ipynb [v0.5.9]
- 设置文件 config.ini 进行用户配置
    * 新增外部播放音频链接，可在 config.ini::player 中自定义播放器地址
    * rootpath 中定义网盘的根目录
    * 支持设置多个禁止删除文件夹 system::nochange, 可设置文件或文件夹，英文逗号隔开，如 nochange=code/,index.html [v0.6.1]
    * 禁止上传 system::allow_file_upload=false [v0.7.0]


# todo
- Markdown 渲染预览
- 上传密码需要在服务端检查
- 可设置：下载也需要密码
- 新建文件夹
- 加入多用户功能，文件能设置私有、公开(需要使用数据库)、按口令公开





# 运行方式 How to run
1. 下载项目 $ git clone https://github.com/BioMooc/webPan.py.git
2. 设置 
 - 安装python3的包 $ pip install flask
 - 如果提示缺少其他包，继续安装缺少的包，比如 $ pip install pkgName
 - webPanLib.py中的rootPath为保存文件的路径(有默认值，但是不一定存在，需要用户核实；如果不可写，则无法上传文件);
 - 修改index.py最后一行为合适的ip和端口号，设置port在 config.ini (用户提供可用端口号，默认值不一定可用);
 - 修改 webPanLib.py 中音频播放器链接地址，推荐用默认地址
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
|-- config.ini 配置文件
|-- static/
    |--css/
        |--webPan.css
    |--js/
        |--main.js
    |--fonts/ 字体文件
    |--images/
|-- templates/ 模板文件
    |--show.html 预览图片
    |--code_reader.html 代码阅读器，显示行号
    |--nbpreview/ jupyter notebook 纯js预览器，一个开源项目的微调
|-- ReadMe.txt 帮助/说明文档
|-- dustbin/ 回收站：上传文件的日志，git不记录
|-- LICENSE 开源协议：MIT，只保留署名权
```

