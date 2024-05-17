#coding=utf-8
import flask, os,sys,time,re, urllib.parse
from webPanLib import *
from flask import request, send_from_directory,redirect,url_for,jsonify,make_response,render_template
import shutil
from flask import send_file
#interface_path = os.path.dirname(__file__)
#sys.path.insert(0, interface_path)  #将当前文件的父目录加入临时系统变量
import re

server = flask.Flask(__name__)


#首页跳转到文件浏览页面
@server.route('/', methods=['get'])
def index():
    return redirect("/list");
#


#download 指定目录下载文件
# v0.2 怎么区分是否在新窗口打开？
@server.route('/download', methods=['get'])
def download():
    fpath = request.values.get('path', '') #获取文件路径
    fname = request.values.get('filename', '')  #获取文件名
    fpathT = os.path.join(rootPath, fpath) #真实路径
    if fname.strip() and fpath.strip():
        #print(fname, fpath);
        if os.path.isfile(os.path.join(fpathT,fname)): # and os.path.isdir(fpath):
            #response = make_response(send_from_directory(fpathT, fname, as_attachment=False))
            #response.headers["Content-Disposition"] = "attachment; filename="+fname.format(fpathT.encode().decode('utf-8'))
            #return response;
            return send_from_directory(fpathT, fname, as_attachment=True) #返回要下载的文件内容给客户端
        else:
            return '{"msg2":"参数不正确"}path=%s, filename=%s;' %(fpathT, fname);
    else:
        return '{"msg1":"请输入参数"}'
#





# 预览图片
@server.route('/show/', methods=['GET'])
def show_photo():
    url = request.values.get('url', '')
    return render_template("show.html", url=url)
#


# 预览代码
@server.route('/code_reader/', methods=['GET'])
def code_reader():
    url = request.values.get('url', '')
    return render_template("code_reader.html", file=url)
#


# 预览 jupyter notebook
@server.route('/nbpreview/', methods=['GET'])
def nbpreview():
    return render_template("nbpreview/index.html")
#



##############
# 支持跨域访问
# version: 0.2
# version: 0.3 支持pdf预览
# version: 0.4 为了兼容高版本 flask, 去掉 send_file() 第一个参数名
##############
#路径名字不能是/static/,因为它是内部定义过的静态文件路径
@server.route('/file/<path:filePath>', methods=['get'])
def audio(filePath):
    #fpath = request.values.get('path', '') #获取文件路径
    #fname = request.values.get('filename', '')  #获取文件名
    fpathT = os.path.join(rootPath, filePath) #真实路径
    print(fpathT)
    if filePath.strip():
        if os.path.isfile(fpathT):
            #blob=''
            #try:
            #    with open( fpathT, 'rb') as file:
            #        blob = file.read()
            #except Exception as e:
            #    print(e)
            #    pass
            
            #res = make_response(blob)
            #res.mimetype='application/octet-stream'
            #res.headers['Access-Control-Allow-Origin'] = '*'
            #return res;
            
            response = make_response(send_file( fpathT, as_attachment=False))
            response.headers["Access-Control-Allow-Origin"]="*"
            return response
        else:
            return '{"msg2":"参数不正确"}path=%s, filename=%s;' %(fpathT, fname);
    else:
        return '{"msg1":"请输入参数"}'
#ajax test OK: http://127.0.0.1:8005/file/tmp.R




# 删除文件 ajax方式
# 删除到dustbin文件夹
@server.route('/delete', methods=['POST'])
def delete():
    fpath = request.form.get('path', '') #获取文件路径
    fnameStr = request.form.get('filenames', '')  #获取文件名
    #return '{"del_msg0":"参数"}path=%s, filename=%s;' %(fpath, fname);
    
    fnameArr=re.split('\,', fnameStr) #分为数组
    rs=""
    for fname in fnameArr:
        #print(fname)
        fpathT = os.path.abspath( os.path.join(rootPath, fpath) ) #真实路径
        if os.path.isfile(os.path.join(fpathT,fname)): # and os.path.isdir(fpath):
            curFile=os.path.join(fpathT, fname);
            #如果不存在垃圾箱，则新建垃圾箱
            dustbin=os.path.abspath( os.path.join(rootPath, "dustbin") );
            if not os.path.exists(dustbin):
                os.mkdir(dustbin)
            #如果不在垃圾箱，则移动到垃圾箱
            
            #rs+="; dustbin="+dustbin +"; fpath="+fpathT+'; ';
            if(dustbin!=fpathT):
                shutil.move(curFile, os.path.join(dustbin,fname) );
                rs+=fname+' moved to /dustbin/, ';
            else:
                os.remove(curFile);
                rs+=fname+' removed, ';
        else:
            return jsonify({"msg": "参数不正确", "path": fpath, 'filename': fname});
    return jsonify({'msg': "deleted!", 'filename': rs});
#





# get方法：查询当前路径下的所有文件
# v0.2 对文件按时间倒序排序
@server.route('/list', methods=['get'])
def getfiles():
    debug='';
    
    fpath = request.values.get('fpath', './') #获取用户输入的目录

    # 空地址自动回首页
    if fpath=="":
        fpath="./"
    if fpath[-1]!="/":
        fpath+="/";
    
    #debug+=fpath;
    
    #保护目录: 保证只能传入相对路径
    if not fpath.startswith("."):
        if fpath.startswith("/"):
            fpath='.'+fpath;
        else:
            fpath='./'+fpath;
    #
    #如果路径出现../开头或者路径中出现/../字样，报非法，返回首页。
    if fpath.startswith("../") or (re.search("\/\.\.\/", fpath)!=None):
        return "<a href='/list'>Go Home</a> <br>Invalid '..' detected in fpath, please use valid path! <br>"+fpath;
    #
    fpathT=os.path.join(rootPath, fpath); #真实地址
    debug+="<div id=fpath style='display:none;'>"+fpath+"</div>";
    #生成顶部路径超链接
    #str to arr, by the end of path
    sep=fpathT[-1];
    arr=re.split(sep, fpath);
    #arr to a links
    url="/list?fpath="
    urlPath="<a id=root href=/list>/RootDir</a>/";    
    for i in range(len(arr)-1 ):
        if arr[i]=='.':
            continue;
        if i<len(arr)-2:
            url=url+ arr[i]+"/";
            urlPath+="<a href="+url+">"+arr[i]+"</a>/"
        else:
            urlPath+=arr[i]+"/";
        #print(i, arr[i], urlPath)
    topPath="<h4 class=root><span><a id='delete' class=button href='javascript:void(0);'>Delete</a></span> Index of "+urlPath+"</h4>\n\n"; #cut to pieces.

    #返回上一级的url链接和tr
    htmlBack="";
    if fpath!="./":
        arr=re.split('/',fpath);
        urlBack="/".join(arr[:-2])+"/";
        htmlBack="<tr class=header><td></td> <td>"+img['back']+" <a title='点击返回上一级' href='/list?fpath="+urlBack+"'>..</a>"+"</td>  <td></td>  <td></td> <tr>\n"
    #tr 文件和文件夹
    htmlF="";
    htmlD="";
    table1="<div class=wrap><fieldset> <legend>File List</legend> "+topPath+"\
<table><tr class=header> <th></th> "+\
"<th>"+img['order']+"FileName</th>   <th>"+img['order']+"Size</th>   <th>"+img['order']+"Modified</th> </tr>\n"
    if os.path.isdir(fpathT):
        filelist = os.listdir(fpathT)
        #为文件增加时间2列，类型列，大小,url
        filelist2d=[]
        for i in range(len(filelist)):
            file=filelist[i];
            url=os.path.join(fpath, file); #显示用虚拟文件路径
            urlT=os.path.join(fpathT, file); #获取都要用真实路径
            arrTime=getModifiedTime(urlT);#真实路径获取时间 ['2019-04-17 09:13:35', 1555463615.2421255]
            #
            type=''
            if os.path.isfile(urlT):
                type='file'
                Size=getDocSize(urlT);
            elif os.path.isdir(urlT):
                type='dir'
                Size=formatSize(dirSize(urlT));#递归计算文件夹大小
            #合并
            filelist2d.append([file, arrTime[0],arrTime[1], type,Size,url])
        filelist2d.sort(key=lambda x:-x[2]) #按时间降序
        #print('3===>', filelist2d,'\n')
        
        for i in range(len(filelist2d)):
            arr=filelist2d[i]
            #['tmp.R', '2019-10-25 13:28:17', 1571981297.2041583, 'file', '17.36kb', './tmp.R'],
            file=arr[0]; #文件名，如果过长，尝试截断显示：优先用js实现
            
            #fix: 在url中的文件名不能含有+号，要替换几个关键字符
            fileInURL=re.sub("\%", "%25", file);
            fileInURL=re.sub("\+", "%2B", fileInURL); 
            fileInURL=re.sub("\&", "%26", fileInURL);
            fileInURL=re.sub("\#", "%23", fileInURL);
            fileInURL=re.sub("\=", "%3D", fileInURL);
            
            fTime=arr[1];
            fTimeNum=arr[2];
            fType=arr[3]
            Size=arr[4]
            url=arr[5]
            #
            if fType=='file': #type="file"
                # 外链地址
                urlPath_out="<a href='/file/"+fpath+fileInURL+"'><i class='fa fa-external-link' style='margin-left:10px;' title='外链 - 请右击复制'></i></a>";
                
                # 文件的后缀名
                arr=re.split('\.', file)
                suffix=arr[len(arr)-1].lower()
                
                
                # setting icon by suffix
                if suffix in ['png', 'jpg', 'jpeg', 'bmp', 'gif','svg']:
                    icon=img['png']
                elif suffix in ['pdf', 'PDF']:
                    icon=img['pdf']
                elif suffix in ['html', "htm"]:
                    icon=img['html']
                elif suffix in ['mp3', "wav"]:
                    icon=img['audio']
                elif suffix=='mp4':
                    icon=img['mp4']
                elif suffix=='txt':
                    icon=img['txt']
                
                elif suffix in [ 'ipynb']:
                    icon=img['note']
                elif suffix in [ 'py']:
                    icon=img['py']
                elif suffix in ["r", "rmd"]:
                    icon=img['R']
                elif suffix in [ 'php']:
                    icon=img['php']
                elif suffix in ["php", "pl", "sh", 'c', 'cpp']:
                    icon=img['code']

                elif suffix in ["rar", "zip", "gz"]:
                    icon=img['rar']
                
                elif suffix in ["doc", "docx"]:
                    icon=img["doc"]
                elif suffix in ["ppt", "pptx"]:
                    icon=img["ppt"]
                elif suffix in ["xls", "xlsx", "csv"]:
                    icon=img["xls"]

                elif suffix in ["conf", "css", "yaml", "yml"]:
                    icon=img["conf"]
                elif suffix in ["js"]:
                    icon=img["js"]
                elif suffix in ["bat"]:
                    icon=img["bat"]

                else:
                    icon=img['file']
                #

                # 预览图标与地址, suffix in lower case
                picViewPath=""
                if suffix in ['png', 'jpg','jpeg','bmp', 'gif', 'svg', 'pdf', 'html', 'mp3', 'mp4']:
                    picViewPath="<a target=_blank href='/show/?url=/file/"+fpath+fileInURL+"'><i class='fa fa-picture-o' style='margin-left:10px;' title='预览 - 单击预览'></i></a>";
                # 预览文本: plain text
                elif suffix in ["txt", "csv", "ini", "config", "gitignore"]:
                    picViewPath="<a target=_blank href='/file/"+fpath+fileInURL+"'><i class='fa fa-picture-o' style='margin-left:10px;' title='预览 - 单击预览'></i></a>";
                # 预览代码 code
                if suffix in ['py', 'r', "c", "cpp", "c++", "h", "sh", "js", "pl", "rmd", "php"]:
                    picViewPath="<a target=_blank href='/code_reader/?file=/file/"+fpath+fileInURL+"'><i class='fa fa-code' style='margin-left:10px;' title='预览代码 - 单击预览'></i></a>";
                # 预览 jupyter notebook
                if suffix in ["ipynb"]:
                    picViewPath="<a target=_blank href='/nbpreview/?filename=/file/"+fpath+fileInURL+"'><i class='fa fa-code' style='margin-left:10px;' title='预览代码 - 单击预览'></i></a>";

                # 播放音频图标 music
                audioPlayPath=""
                if suffix in ['mp3', 'wav']:
                     audioPlayPath="<a target=_blank href='"+playerPath+ \
                     request.host_url + \
                     "file/"+strip(fpath, "^\./")+fileInURL+"'><i class='fa fa-play-circle-o' style='margin-left:10px;' title='播放 - 单击新标签页播放'></i></a>";
                
                #
                htmlF+="<tr class=file data-time='"+str(fTimeNum)+"'> <td><input type='checkbox' tabindex='-1'></td> <td>"+icon+" <a title='点击下载' target='_blank' href='/download?filename="+fileInURL+"&path="+fpath+"'>"+file+'</a> '+urlPath_out+picViewPath+ audioPlayPath+ "</td>  <td>"+Size+"</td>   <td>"+fTime+"</td>  </tr>\n"
            elif fType=='dir': #type="dir"
                htmlD+="<tr class=dir data-time='"+str(fTimeNum)+"'> <td><input type='checkbox' tabindex='-1'></td> <td>"+img['dir']+" <a title='点击打开' href='/list?fpath="+url+"/'>"+file+"/</a></td> <td>"+Size+"</td>  <td>"+fTime+"</td>  </tr>\n"
    #files = [file for file in filelist if os.path.isfile(os.path.join(fpath, file))]
    return head+debug+table1+htmlBack+htmlF+htmlD+"</table> </fieldset></div>"+foot;









# post方法：上传文件的 https://www.cnblogs.com/wl443587/p/10552542.html
@server.route('/upload', methods=['POST'])
def upload():
    fname = request.files.get('file')  #获取上传的文件
    uploadDir = request.form['uploadDir'] #获取上传的路径
    uploadDir = request.form.get('uploadDir','./') #获取上传的路径
    #return uploadDir;
    
    ip = request.remote_addr
    
    if fname:
        url=url_for('getfiles',fpath=uploadDir );
        
        # fix: 禁止文件名包含&，否则会导致下载失败
        #if re.search('&', fname.filename) != None:
        #    #return '{"msg": "文件名不能包含特殊符号 & (请去掉该符号后重新上传)"}'
        #    return '<meta http-equiv="refresh" content="3;url='+url+'">'+"<span style='color:red;'>Failed!</span> <br><b style='font-size:30px;'>delete & in your filename and upload again.</b> <br>Returning to list in 5 seconds.<br>";
        
        t = time.strftime('%Y%m%d%H%M%S')
        new_fname = os.path.join(rootPath, uploadDir, fname.filename);
        if os.path.exists(new_fname): #如果存在，则加时间戳前缀
            new_fname = os.path.join(rootPath, uploadDir, t +'_'+ fname.filename);
        fname.save(new_fname)  #保存文件到指定路径
        
        #logger
        if not os.path.exists('dustbin'):
            os.mkdir('dustbin')
        with open("dustbin/upload.logger.txt", 'a', encoding='utf-8') as f:
            timsString=time.strftime("%Y/%m/%d-%H:%M:%S", time.localtime()) 
            f.write('\t'.join([timsString, ip, fname.filename, new_fname])+"\n" )
        
        #return url;
        return '<meta http-equiv="refresh" content="3;url='+url+'">'+"Upload Success!. Returning to list in 3 seconds.<br>";
    else:
        return '{"msg": "上传文件不能为空！(请先选择上传文件)"}'



# 添加新静态文件的路径，这样就允许xx/下的图片加载了
@server.route("/static/<path:filename>")
def downloader(filename):
    return send_from_directory("static",filename,as_attachment=False)

# 添加新静态文件的路径，这样就允许 nb/下的css/js资源加载了
@server.route("/nbpreview/<path:filename>")
def nbpreview_src(filename):
    return send_from_directory("templates/nbpreview/",filename,as_attachment=False)



# 几个在linux终端打印彩色文字的函数
def print_yellow(str):
    print( f"\033[40;33m{str}\033[0m" )
def print_red(str):
    print( f"\033[40;31m{str}\033[0m" )

# for win cmd
# https://www.delftstack.com/howto/python/python-print-colored-text/
# https://github.com/tartley/colorama
def print2(color, str):
    if env=="linux":
        if color=="red":
            print_red(str)
        else:
            print_yellow(str)
    elif env=="win32":
        import colorama
        from colorama import Fore
        from colorama import Style
        colorama.init()
        if color=="red":
            print(Fore.RED + Style.BRIGHT + str + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + Style.BRIGHT + str + Style.RESET_ALL)
    else:
        print(str);


# run the app
if __name__ == '__main__':
    server.debug = True # 设置调试模式，生产模式的时候要关掉debug
    # env defined in webPanLib.lib
    port = 8000 if env=="linux" else 8005
    #     ubuntu                    windows
    
    # 显示欢迎屏
    print2("yellow", "#"*45);
    print2("yellow", "#    Welcome to webPan.py                   #");
    print2("yellow", f"#       * Version: {version}                   #" )
    print2("yellow", f"#       * Environment: {env}                #" )
    print2("red", f"#       * URL: http://127.0.0.1:{port}        #" )
    print2("yellow", f"#    https://github.com/BioMooc/webPan.py   #" )
    print2("yellow", "#"*45);
    
    server.run(host="0.0.0.0",port=port)
#