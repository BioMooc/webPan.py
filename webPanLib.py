#coding=utf-8
# lib for the app 
# const, function, class

import os,time

#设置变量
import sys
env=sys.platform #"win32"测试环境;  "linux"生产环境
#print('env=',env)
if env=='linux':
    rootPath="/home/wangjl/web/docs/" #ubuntu
elif env=='win32':
    rootPath="F://Temp/" #windows

version="v0.3.1"
head='''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width" />
    <meta http-equiv=Content-Type content="text/html;charset=utf-8">
    <title>webPan.py - Mini网盘
%s
    </title>
    <link rel="shortcut icon" href="/static/images/favicon.ico">
    <link rel="stylesheet" href="/static/css/webPan.css" />
    
    <!-- 外链图标 -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">
</head>

<body>
<div class="wrap">
    <h1><img src="/static/images/webpan_simple.png" style="height:40px; padding:0 10px;">webPan.py</h1>
</div>


<div class="wrap">
    <fieldset>
        <legend>Upload File</legend>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" />
            <input type="hidden" name="uploadDir" value="." />
            <input type="submit" value="上传" /> 
            <span style='margin-left:30px;'>注意: 本网盘只是临时中转，请及时备份！超过一周的文件可能随时会被<b style='color:red;'>删除</b>！</span>
        </form>
    </fieldset>
</div>

'''
head=head % version;

foot='<div class="wrap footer"> \
    <p>&copy;2020 webPan.py \
%s \
| <a target=_blank href="https://github.com/DawnEve/webPan.py">Fork Me</a> | RootPath('+rootPath+')</p> </div> \
<script src="/static/js/main.js"></script> \
</body> </html>'
foot=foot % version;


img={
    "file":'<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACAklEQVR42u2XyUsDMRTGe3S5OpNSipP0oEkKXgQRBBE33BARRYqIIIKIIIgIggcR3HBB646IuG+H4oK1tC4V/Z96rO+BcxEmLm3m5IM5DUN+yfu+72U8ni9VEOBFxApWk0JZYwZErclEncl4vUGDDYYlmgos0UwCvIUw2WpS0WZavN1gwQ6DyU5CRRehPORlsoxSmuP5S+Hi6QzqKnKTTr69RwCm/E8QuPNMAVKpVPr59f3aLCyu8Pv9ub8CwGPPFAALIRJPyTuDicpfQWC/swFgQ8Sfkvdeyqt8vtK8HwGg2LIFYEPEEs8PeLI/gjAs2ZhNABviPhaP4+l+C4FWyzaADXEXjT3iBgkpyXd2AXhcB4ANcRuNveAazgAQMJkCzC2Fv32cXQDpltZcBuMzzgAQrboBYJPzziKEXNcOYPFFZw3AQNEOwOSyAoCHtGuAilWFBmS3bgBi8TXFLBA9+lsgNhSzgPe64IIt1Szo0w/AdxRJKPr121DsKpJQDuhPQrGniuJB7S6gfF81jodcEOGBwgVy2AUNHKmieMQFgGPVNBzV3wJ5qkrCMRc0cKZKwnEXhtGF4tdMTOi3obhU3oohKiehT1MQGNOEylm8wYBwFnCOA/0K+DhMLLkO7dqEd9sYrZhuGDDocbQZPIeodriKn+CRw3fnuHNcHNPW81+f9QFiij/qVroAPQAAAABJRU5ErkJggg==">',
    
    "dir": '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABn0lEQVR42u2XvUsCYRzHH5WgN3r5K5qDotGhpamtrSFobGxrEWqwUI9DQwOJIFoSWsrTpEFEMgQjwigSkSQxTau78336dScYij5Kl7+jwS98hufgnu+H51l+DyGD9CEGA9G6jWS6Gy4X0aGUcwyZ4xgt+PanuuJhdBJE39dyr5nMy+XxWwf0ylPEWZfgTGShz+UH9YJsPgfpbKYrDzdWkP/xWMhs24YARNPrHhsoKW8QvTYDZ9GAlyUzLeXyx1732IyS8gb3gR3pJAj7I3C1SyZ9tgn4bZSUy7ymYtIpEL5F4FIS4AVB0YZ/EnBbiF1agBqEL9baBXy2cVArskRHgVohBKX8MTp0ATEIpfdDdCgCY1Dj/VB6c6BDFah+XkExxaJDF/jwQDG5hw5dIHcOhcQ2Op0FrKNQzZxBIbaFDlWgkj4F8XETHbpA6gTE6AY6FIERqCSPQLxbR4cqUH5xghBZRYcukLCDEF5Bhy4QtwIfWkaHLhBjgA8uoUMRGIbyswn4wCI6nQXYIfjy61WhaTjhpZnQqPpEJHcN3pH/Lt8WJRscHbhvPQAAAABJRU5ErkJggg==">',
    
    'back': '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAv0lEQVR42mNgGAVEApH5EfWi8yP+gzCIPSCWu1/t+W9xtpG+jkC23OfWxP82l1r/qxwupI8j0C2HOUDteAntHYHNcmQH0NQRuCxHdwBNHIHPcmwOoKojCFmOywFUcQQxluNzAMWOIMZyQg5AdgRZDiBkOTEOAGGyHYAN62zPx+kAmfUp/3Hpo1qWRA8ZZAdQ1aJRB4w6YNQBQ9IB+AoiqhVQ+BxAKh51ANkOwNYopZsDxOZHNJCa0KiaCEfBsAcAEh85/7c92uEAAAAASUVORK5CYII=">',
    
    'order':'<img title="order" id=order src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAHCAYAAADebrddAAAAiklEQVR42mPIrewMya3oup5X2XkeiC/nVXRezgViEDu3vPMskH0BROeVdqkyJNTXcwAlDgDxfwxcAaWrOpsYYCC/qlUcKPgMLlnZBcWd/4E272BAB0DdjkDJf2AFFRBTgfTj4uIeEQZsAKigHmE6EJd32DDgA0DF20FOyK/sqmIgBEDWAhVPwyYHAJAqZIiNwsHKAAAAAElFTkSuQmCC" style="width:11px;height:9px;">'
    
};


# 字节bytes转化kb\m\g
#v0.2 保留2位
def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.2fG" % (G)
        else:
            return "%.2fM" % (M)
    else:
        return "%.2fkb" % (kb)


# 获取文件大小
def getDocSize(path):
    try:
        size = os.path.getsize(path)
        return formatSize(size)
    except Exception as err:
        print(err)


# 获取文件夹大小，递归法，返回的是bytes，需要在最终返回值做k/m/g换算
# by: Lin Yanling v0.1 2019.9.4
# v0.2 改为os.path.join
def dirSize(path):
    content = os.listdir(path)
    size = 0
    for v in content:
        if os.path.isfile('/'.join([path,v])):
            size += os.path.getsize(os.path.join(path, v)); #'/'.join([path,v])
        else:
            size += dirSize(os.path.join(path, v)) #'/'.join([path,v])
    return size
#

#获取修改时间
def getModifiedTime(full_path):
    mtime = os.stat(full_path).st_mtime;
    file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime));
    return [file_modify_time, mtime];