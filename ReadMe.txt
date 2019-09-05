# 网盘 webPan.py 练手版(Python3)

OS: win10, Ubuntu 1804


# 现有功能
在webPanLib.py中定义根目录
浏览和下载文件
上传文件
删除一个或多个文件





# 运行方式
1.下载项目；
2.设置 
(1)webPanLib.py中的rootPath为存在的路径;
(2)修改index.py最后一行为合适的ip和端口号;

3.运行 $ python index.py  #会提示url
4.在浏览器打开使用。





# 项目文件结构
|-- index.py 入口文件
|-- webPanLib.py 定义函数和常量
|-- static/
    |--css/
        |--webPan.css
    |--js/
        |--main.js
|-- ReadMe.txt 说明文档
#






# change log:
v0.0.1 只能列举运行目录的地址。
v0.0.2 可以自定义路径了
v0.0.3 主体用table改造，对齐
v0.0.4 顶部路径去掉.\符号，改为./; 入口改名为index.py
v0.0.5 添加上一级目录功能;添加上传文件功能
v0.0.6 安全问题，避免访问..或者xx/../../之类的文件夹。如果路径中有两点，则报错。
v0.0.7 加了边框; 加了复选框;
v0.0.8 加了头部和底部
v0.0.9 ReadMe添加运行方式
v0.1.0 添加github链接
v0.1.1 行按照时间排序
v0.1.2 使用Rstudio风格界面色彩
# # -----------------> git push origin master
v0.1.3 递归获取文件夹大小
v0.1.4 删除文件，js传输，ajax实现; 删除键红色字体显示;
v0.1.5 删除文件前使用js二次确认
# commited here.





todo:
4.多用户，回收站5天后删除。


done:
1.指定目录当根目录。[done v0.0.2]
2.上传文件[done v0.0.5]
3.删除文件，使用js二次确认。[done v0.1.5]

