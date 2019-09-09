# 网盘 webPan.py

用于局域网内文件短暂共享，可以不用U盘了。

todo 加入多用户功能，文件能设置私有、公开(需要使用数据库)

![screenShot0.1.6](./static/images/webPan_py.png)


# 环境
- Python3 flask
- testOS: win10, Ubuntu 1804
- version: 0.1





# 现有功能
- 在webPanLib.py中定义根目录
- 浏览和下载文件
- 上传文件
- 删除一个或多个文件





# 运行方式
1. 下载项目；
2. 设置 
 - 安装python3的包 $ pip install flask
 - webPanLib.py中的rootPath为存在的路径;
 - 修改index.py最后一行为合适的ip和端口号;
3. 运行 $ python index.py  #会提示url
4. 在浏览器打开url。





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
```

