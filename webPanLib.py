#coding=utf-8
# lib for the app 
# const, function, class

import os,time, re


#########################
# settings
#########################
#设置变量
import sys
env=sys.platform #"win32"测试环境;  "linux"生产环境
#print('env=',env)
if env=='linux':
    rootPath="/home/wangjl/data/web/docs/" #ubuntu
elif env=='win32':
    #rootPath="F://Temp/" #windows
    #rootPath="G://baiduDisk//" #windows
    rootPath="G://xampp//htdocs//DawnScholar//audio" #windows

version="v0.4.6"


# 音频播放器地址
playerPath="http://ielts.biomooc.com/listening/player.html?url="





#########################
# web pages
#########################

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
    
    <!-- 外链图标 
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">
    -->
    <link rel="stylesheet" href="/static/css/font-awesome.min.css">
    
</head>

<body>
<div class="wrap">
    <h1><img src="/static/images/webpan_simple.png" style="height:40px; padding:0 10px;">webPan.py</h1>
</div>


<div class="wrap">
    <fieldset>
        <legend>Upload File</legend>
        <form action="/upload" method="post" enctype="multipart/form-data" id="oBtnForm">
            <input type="file" name="file" id="file" draggable="true" class="fileBox" />
            <input type="hidden" name="uploadDir" value="." />
            <input type="submit" id="submit" value="上传(Upload)" /> 
            <span style='margin-left:30px;'>注意: 本网盘只是临时中转，请及时备份！超过一周的文件可能随时会被<b style='color:red;'>删除</b>！</span>
        </form>
    </fieldset>
</div>

'''
head=head % version;

foot='<div class="wrap footer"> \
    <p>&copy;2020-2021 webPan.py \
%s \
| <a target=_blank href="https://github.com/DawnEve/webPan.py">Fork Me</a> | RootPath('+rootPath+')</p> \
chrome://flags/#block -Secure private network requests | Disabled, Relaunch\
</div> \
</body> \
    <script src="/static/js/main.js"></script> \
    <script src="/static/js/drag_upload.js"></script> \
</html>'
foot=foot % (version);


img={
    "file":'<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACAklEQVR42u2XyUsDMRTGe3S5OpNSipP0oEkKXgQRBBE33BARRYqIIIKIIIgIggcR3HBB646IuG+H4oK1tC4V/Z96rO+BcxEmLm3m5IM5DUN+yfu+72U8ni9VEOBFxApWk0JZYwZErclEncl4vUGDDYYlmgos0UwCvIUw2WpS0WZavN1gwQ6DyU5CRRehPORlsoxSmuP5S+Hi6QzqKnKTTr69RwCm/E8QuPNMAVKpVPr59f3aLCyu8Pv9ub8CwGPPFAALIRJPyTuDicpfQWC/swFgQ8Sfkvdeyqt8vtK8HwGg2LIFYEPEEs8PeLI/gjAs2ZhNABviPhaP4+l+C4FWyzaADXEXjT3iBgkpyXd2AXhcB4ANcRuNveAazgAQMJkCzC2Fv32cXQDpltZcBuMzzgAQrboBYJPzziKEXNcOYPFFZw3AQNEOwOSyAoCHtGuAilWFBmS3bgBi8TXFLBA9+lsgNhSzgPe64IIt1Szo0w/AdxRJKPr121DsKpJQDuhPQrGniuJB7S6gfF81jodcEOGBwgVy2AUNHKmieMQFgGPVNBzV3wJ5qkrCMRc0cKZKwnEXhtGF4tdMTOi3obhU3oohKiehT1MQGNOEylm8wYBwFnCOA/0K+DhMLLkO7dqEd9sYrZhuGDDocbQZPIeodriKn+CRw3fnuHNcHNPW81+f9QFiij/qVroAPQAAAABJRU5ErkJggg==" width="16" height="16" alt="PDF">',
    
    "pdf":'<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACtUlEQVR42u2X60sUURjGV9hwd72turra5V/oS5+iD0kXCMIKuiJUUtAFFiLBL11Y0yIh1C5i2QWlsKT7TaHa2hDCMNaKQspEotR2HGdWZXZ1dmd8OudItqlr7c60QfXAwwzDzJzfvOe8z8wYDBF0sLS8YH/p0dpYTK8tKSmxGLSI3ggxyu12M2uCiBVAURQ2uNfr7dEEESuAJEkMgOqXIF7mzMVkt+fMQUV6Jtrss/Hcnotn2bloycqB22aHy5aNB5lZaMqw4S4556Y1A9fS0nEl1coG5Xl+AiAcYm9lpTkigDdvqWZfTEllA3Ic9wMAVd9MEHoBnJplROjDewbgcrmmTE1ECFpuPQBqzGaoAh8RIBzC6XSaJgBekHnWA6AqMRHK508zAkwL0UoWmB4A5UYjlN6enwJMgaCrWw+A0oQEjMmjEEURHo+HQYT7WziFmyam4TFpq4ekrZpJW90jbXWLtNV1azqKk5LQkJrGVnddcgrOJyWjlhyrsVhQTXySzPlxapMJVcRlBIBKlmUGQSsx2bRFaU7QsKKiWaNLEKncF/TaTQh1vI0qtHQDkM6cwMDqZRjcV/RnAPqXL2RV4POXsG1cAeS2VgiFG8b3PW0QNq2ib6T4AYi7tmD06fe2k+pqIWxdh7GA//cDhLo6wa/Mm3I8cKMR/YsXwN94iVk6Vw2p/ixGmu5AHRrUD0DcuXn86UnJR1ueYPhYGVuIg8UODFccgW/PDvTNS4PPsR2Bqw2sOj7HNn0Agq/bwS2aj5H7t+G/XI/gK8+0c694+1gF6MBDhw9g5FGzdgDVJ2JgYz5Cne+gRVEDqKIA6cJp9kTD5YegVVEBqDwHX9FuhLq7MLB2Bcl9Ob4AQsEa9sFBt8rHbuihqABovwuF6xHseAO9pFsU/wf4OwG0/JxG8xNr+Of1FTogGCx+iM12AAAAAElFTkSuQmCC" border="0" width="16" height="16" alt="PDF">',
    
    "png": '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAH1ElEQVR42uWW+VNUVxqGD0mbxS0xQQd1yiWJqViOzhgziYmOjlqlhU6caDLqpFwSnSRqFDSKOy4IIuKCqOCKKCpuoAgICArdNA3asgwRUGQRAaEbZRHoZuv7zLn+cPkT+GFu1Vt9+u1z+3nP+b4+t4UhPStIn55JV0hli+Q0M111qWxxx3ivywKobJFkyNCMdzbcou9cXwZ+u4x+P/rRb4k37644RD/3AwzzNfCnw8/QHehAt68V3V47On9VNnR+Tei8G9F5NaDbWofO8wW6DVZ0K+X8VZXo3MrQLX5Mz5UFLDjxVOOpbJGQnKYZY37ZxeD1N+njcZM33WJ4y/MuvXdm8saeQl4/3IFTMIjDUgEK3YPtDDvWRM9DzYh9LTjttyNkGOHbhNjewCd76gm83cg4fyu915QzK7CCC6kNJOW2aDyVLeJup2rG5DGCb0YLRg7vifOgXoyfOoQxa3bx0dqduOzIoJ/3AwYdLGHoiVbeC4EB8nXkMRsDDtlfhRAH2xAH5HhnE2sS7Ngl615hK/elXtQpPKl2EGFu1ngqW8TcStGMj1fuYPyUHnz2RTcmfCn4+zjB4l/fZ/6m0Yz08KanfzaD9+fjFXKNg0d9+PKIhaxKSC1uZ9nNdoacaKFXsI2Bwc1MOF7HthsN1DTASztU1ysYH9nwi7ZoPJUtouJua8aIxasZv+EnXL//lFHTRvDV37oxY/bbzPOaxTafQbjvHMvC07vYZ8gmPv4epqQ4WutLtPuPp7fx1ckW3K40MjO0iclhNjLK2jE9buOcqQ7v688YtrdKm6+yRWTMLc345V9jmOPrR/dTzxnkdYlxK2cydeE7TFg5HZeIZj4ML2XSkWim7juHp96Bo7mBF7XVNLY60Jc4WBLdwcaEVrwTbcy52sq4sDbC79s5bmzAP/4FnhFVjAvqDKCyxZWoOM34yS+Qjcs/5w8RCkOvOXA9E8Vcr2XMDdjK8OgWhkbDaDl9bAx8nwC5VqhoAkOZgxv5HRgetvD7EzuWGjs1lmZyHjfjKXthR3wD66KsrL5cwcLQCo2nssXFyBjNmClXOCfkIa6RHfxT2osTYWliG0v1sCgJfpTVWnZHYXu6QnSRg7waB1cL2gnNbSOxuI0SSyv55S0UlttJKWgm9bGNs+kv+Xd4Je7XyglLruKS8bnGU9ni/JXrmvFDLKyXsOj8dsILFMzVCia5Y9szFPbfd3Awy8G5fIWgHAfmSgcFlnYCMmz4Gps4n91Mlqx3XlUHdwtlgIfNRGU3EmyoZUdcFVH3ariSbuVAXGcJVLY4Ex6hGWcM9YQZX5JZ0MSjUht1tXJVla3kFNkpr7CRX9pMWXUb1joHlS8cFFk6MJW0YC6xc1fOSVXBstPv5Nu4IeEhhjqO658TLld9LKmagNhy3M4/6eRJtgg5d0kz1idWsSm5hi2psmPVrjXWsju9jt3mBvZnvWRPZhP75RcH5TZxOreRU9ILzaznbGYdIWapu7UcNz3nUEoNe5KseMc9wzO6HI/IUlZeLuLnC4/45uQjjaeyxfHQC5rhnJDHgNtZfJJ8j1F6E7PSUnE1GvmzwchfDXq+0OuZZEjB1ZDM0jQ9u8wm1qWn4ZaagntyMmuT7rAuIYkNN+Nxj7rJz5EJLLwcz+zzMcw+G8uMkzeYeLiz6VW2CD51VjPS7x9BnxOJqSAJ85NMHlYUkldaxN2SUrLLK/jv03IeVTyTW1/zSoUWC+ayMlKLijEWFcnfez6GvEwSMxOJMV0lIiWUi4kBhCds5dLN1Vy9sYyQy6s0nsoWh46d7nw8VS2A5z9A7SIonwfW+WBbL+Up/bVQvwUa/KDOV87ZCTXyvdVD6jd49is8XQLFc+DxP6BgIvz+KeR8BFm95ZksIENgud1fw6lsERB0QjOUwvE8CnMmck0PolY5kX9pAMawEcT6OnNrk6A47A1KowdRHPEhtcaPsZdMwV72NW1PpqEUz5CajlI0XcInQ/4EeVCMg8xhKPcHygDdUEwywK3OACpb7A08qhmB8wV75wk8pgjWTha4TRTsni049R/BtQ2vkez/JtlBPcg85UzOibeputaLvNC+1Fzti+PeH1Gyh6DkfYby4HPIG4uSMwIlazCKuRdKmkAxOmFJ7AygsoXfgcOasUg+fFZMEjwMf538GzritzkR+K0MNVdwzk1Hsl9vUn26kxP8BkXndViudadRPxBb2lA67n+AI2ckSu5QuQPOMsC7YH4LJcPp1coVvSyBlCWhM4DKFrv2HtSMzdME3tMFhxY40ZKrkzV/j+r494n3eI2IFYJnETrStzhxVgaKXSZIWC4wrZJaLcjeLKgOkHP2Cp4HCxoineiQcLX2Kly5LQMkywAxnQFUtvDavb/z6bRE4DNT4C53IfQ7QXuqDGHtKZupO23ZfcDSF4r60GJ0oSlWUHNY0HxdKkJQelRQf1HQdFlCpG/1l5JhWq5IuEHC70jJe15cddZ4Klts89nTeTYvdWG5qwvuX7vgMdMFn+9ceBD1AdaCv2B9MIrqzMFYHgyXGoHV7II1VUqGsWZImaTS+stx/1djS0p/uXv9qYyV43j5mVRNdD8KLwzXeCpbbPHy7bI/pSpbbNzm02UBVLZY7+nVZQFUtli7aVuXBVDZ4rcNnl0WQGWLVes2d1kAlS3c1m4MkqKLFCT+76//ATbQGsExWqQKAAAAAElFTkSuQmCC" border="0" width="16" height="16">',

    
    "html": '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAMAAADXqc3KAAAB+FBMVEUAAAA/mUPidDHiLi5Cn0XkNTPmeUrkdUg/m0Q0pEfcpSbwaVdKskg+lUP4zA/iLi3msSHkOjVAmETdJSjtYFE/lkPnRj3sWUs8kkLeqCVIq0fxvhXqUkbVmSjwa1n1yBLepyX1xxP0xRXqUkboST9KukpHpUbuvRrzrhF/ljbwaljuZFM4jELaoSdLtElJrUj1xxP6zwzfqSU4i0HYnydMtUlIqUfywxb60AxZqEXaoifgMCXptR9MtklHpEY2iUHWnSjvvRr70QujkC+pUC/90glMuEnlOjVMt0j70QriLS1LtEnnRj3qUUXfIidOjsxAhcZFo0bjNDH0xxNLr0dIrUdmntVTkMoyfL8jcLBRuErhJyrgKyb4zA/5zg3tYFBBmUTmQTnhMinruBzvvhnxwxZ/st+Ktt5zp9hqota2vtK6y9FemNBblc9HiMiTtMbFtsM6gcPV2r6dwroseLrMrbQrdLGdyKoobKbo3Zh+ynrgVllZulTsXE3rV0pIqUf42UVUo0JyjEHoS0HmsiHRGR/lmRz/1hjqnxjvpRWfwtOhusaz0LRGf7FEfbDVmqHXlJeW0pbXq5bec3fX0nTnzmuJuWvhoFFhm0FtrziBsjaAaDCYWC+uSi6jQS3FsSfLJiTirCOkuCG1KiG+wSC+GBvgyhTszQ64Z77KAAAARXRSTlMAIQRDLyUgCwsE6ebm5ubg2dLR0byXl4FDQzU1NDEuLSUgC+vr6urq6ubb29vb2tra2tG8vLu7u7uXl5eXgYGBgYGBLiUALabIAAABsElEQVQoz12S9VPjQBxHt8VaOA6HE+AOzv1wd7pJk5I2adpCC7RUcHd3d3fXf5PvLkxheD++z+yb7GSRlwD/+Hj/APQCZWxM5M+goF+RMbHK594v+tPoiN1uHxkt+xzt9+R9wnRTZZQpXQ0T5uP1IQxToyOAZiQu5HEpjeA4SWIoksRxNiGC1tRZJ4LNxgHgnU5nJZBDvuDdl8lzQRBsQ+s9PZt7s7Pz8wsL39/DkIfZ4xlB2Gqsq62ta9oxVlVrNZpihFRpGO9fzQw1ms0NDWZz07iGkJmIFH8xxkc3a/WWlubmFkv9AB2SEpDvKxbjidN2faseaNV3zoHXvv7wMODJdkOHAegweAfFPx4G67KluxzottCU9n8CUqXzcIQdXOytAHqXxomvykhEKN9EFutG22p//0rbNvHVxiJywa8yS2KDfV1dfbu31H8jF1RHiTKtWYeHxUvq3bn0pyjCRaiRU6aDO+gb3aEfEeVNsDgm8zzLy9egPa7Qt8TSJdwhjplk06HH43ZNJ3s91KKCHQ5x4sw1fRGYDZ0n1L4FKb9/BP5JLYxToheoFCVxz57PPS8UhhEpLBVeAAAAAElFTkSuQmCC" border="0" width="16" height="16">',

    
    "audio": '<img src="/static/images/icon_mp3.png" border="0" width="16" height="16">',
    "mp4": '<img src="/static/images/icon_mp4.png" border="0" width="16" height="16">',
    
    "note": '<img src="/static/images/notebook.ico" border="0" width="16" height="16">',
    "code": '<img src="/static/images/icon_code.png" border="0" width="16" height="16">',
    "R": '<img src="/static/images/icon_R.png" border="0" width="16" height="16">',
    "rar": '<img src="/static/images/icon_rar.png" border="0" width="16" height="16">',
    
    "txt": '<img src="/static/images/icon_txt.png" border="0" width="16" height="16">',
    "js": '<img src="/static/images/icon_js.png" border="0" width="16" height="16">', #js
    "bat": '<img src="/static/images/icon_bat.png" border="0" width="16" height="16">', # bat
    "conf": '<img src="/static/images/icon_conf.png" border="0" width="16" height="16">', #css, yaml, yml, conf
    
    "doc": '<img src="/static/images/icon_docx.png" border="0" width="16" height="16">',
    "ppt": '<img src="/static/images/icon_pptx.png" border="0" width="16" height="16">',
    "xls": '<img src="/static/images/icon_xlsx.png" border="0" width="16" height="16">',

    
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

# 按正则表达式，去掉某个部分
def strip(str1, reg):
    return re.sub(reg, "", str1)
