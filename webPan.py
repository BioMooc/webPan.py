import flask, os,sys,time,re
from webPanLib import *
from flask import request, send_from_directory,redirect

interface_path = os.path.dirname(__file__)
sys.path.insert(0, interface_path)  #将当前文件的父目录加入临时系统变量


server = flask.Flask(__name__)


#get方法：指定目录下载文件
@server.route('/download', methods=['get'])
def download():
    fpath = request.values.get('path', '') #获取文件路径
    fname = request.values.get('filename', '')  #获取文件名
    fpathT = os.path.join(rootPath, fpath) #真实路径
    if fname.strip() and fpath.strip():
        #print(fname, fpath);
        if os.path.isfile(os.path.join(fpathT,fname)): # and os.path.isdir(fpath):
            return send_from_directory(fpathT, fname, as_attachment=True) #返回要下载的文件内容给客户端
        else:
            return '{"msg2":"参数不正确"}path=%s, filename=%s;' %(fpathT, fname);
    else:
        return '{"msg1":"请输入参数"}'
#

@server.route('/', methods=['get'])
def index():
    return redirect("/list");
#



# get方法：查询当前路径下的所有文件
@server.route('/list', methods=['get'])
def getfiles():
    fpath = request.values.get('fpath', '.') #获取用户输入的目录
    fpathT=os.path.join(rootPath, fpath); #真实地址
    
    #str to arr, by the end of path
    sep=fpathT[-1];
    arr=re.split(sep, fpath);
    #arr to a links
    url="/list?fpath="
    urlPath="<a class=root href=/list>根目录</a> "
    for i in range(len(arr)-1 ):
        url=url+arr[i]+"/"
        urlPath+="<a href="+url+">"+arr[i]+"</a>/"
        #print(i, arr[i], urlPath)
    titlePath="<h4>Path: "+urlPath+"</h4>\n\n"; #cut to pieces.

    #
    htmlF="";
    htmlD="";
    if os.path.isdir(fpathT):
        filelist = os.listdir(fpathT)
        for i in range(len(filelist)):
            file=filelist[i];
            url=os.path.join(fpath, file); #显示用虚拟文件路径
            urlT=os.path.join(fpathT, file); #获取都要用真实路径
            fTime=getModifiedTime(urlT);#真实路径获取时间
            #
            if os.path.isfile(urlT): #type="file"
                fSize=getDocSize(urlT);
                htmlF+="<li class=file>"+imgFile+file+"<a target='_blank' href='/download?filename="+file+"&path="+fpath+"'>下载</a> <span>"+fSize+"</span>   <span>"+fTime+"</span>  </li>"
            if os.path.isdir(urlT): #type="dir"
                htmlD+="<li class=dir>"+imgDir+file+"/ <a href='/list?fpath="+url+"/'>打开</a>   <span>"+fTime+"</span>  </li>"
        #files = [file for file in filelist if os.path.isfile(os.path.join(fpath, file))]
    return title+css+titlePath+"<ol>"+htmlF+htmlD+"</ol>";


# post方法：上传文件的
@server.route('/upload', methods=['post'])
def upload():
    fname = request.files.get('file')  #获取上传的文件
    if fname:
        t = time.strftime('%Y%m%d%H%M%S')
        new_fname = r'upload/' + t + fname.filename
        fname.save(new_fname)  #保存文件到指定路径
        return '{"code": "ok"}'
    else:
        return '{"msg": "请上传文件！"}'



# 添加新静态文件的路径，这样就允许data/下的图片加载了
@server.route("/static/<path:filename>")
def downloader(filename):
    return send_from_directory("static",filename,as_attachment=False)



# run the app
if __name__ == '__main__':
    server.debug = True # 设置调试模式，生产模式的时候要关掉debug
    server.run(host="127.0.0.1",port=8005) #default