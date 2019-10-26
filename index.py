import flask, os,sys,time,re, urllib.parse
from webPanLib import *
from flask import request, send_from_directory,redirect,url_for,jsonify,make_response 
import shutil

#interface_path = os.path.dirname(__file__)
#sys.path.insert(0, interface_path)  #将当前文件的父目录加入临时系统变量

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


##############
# 支持跨域访问
# version: 0.2
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
            blob=''
            try:
                with open( fpathT, 'rb') as file:
                    blob = file.read()
            except Exception as e:
                print(e)
                pass
            #
            res = make_response(blob)
            res.mimetype='application/octet-stream'
            res.headers['Access-Control-Allow-Origin'] = '*'
            return res;
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
    if fpath[-1]!="/":
        fpath+="/";
    
    #debug+=fpath;
    
    #保护目录，保证只能传入相对路径
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
    urlPath="<a href=/list>(RootDir)</a>/";
    for i in range(len(arr)-1 ):
        if arr[i]=='.':
            continue;
        if i<len(arr)-2:
            url=url+ arr[i]+"/";
            urlPath+="<a href="+url+">"+arr[i]+"</a>/"
        else:
            urlPath+=arr[i]+"/";
        #print(i, arr[i], urlPath)
    titlePath="<h4 class=root><span><a id='delete' class=button href='javascript:void(0);'>Delete</a></span> Index of "+urlPath+"</h4>\n\n"; #cut to pieces.

    #返回上一级的url链接和tr
    htmlBack="";
    if fpath!="./":
        arr=re.split('/',fpath);
        urlBack="/".join(arr[:-2])+"/";
        htmlBack="<tr class=header><td></td> <td>"+img['back']+" <a title='点击返回上一级' href='/list?fpath="+urlBack+"'>..</a>"+"</td>  <td></td>  <td></td> <tr>\n"
    #tr 文件和文件夹
    htmlF="";
    htmlD="";
    table1="<div class=wrap><fieldset> <legend>File List</legend> "+titlePath+"\
<table><tr class=header> <th></th> <th>FileName</th>   <th>Size</th>   <th>"+img['order']+"Modified</th>  </tr>\n"
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
        print('3===>', filelist2d,'\n')
        
        for i in range(len(filelist2d)):
            arr=filelist2d[i]
            #['tmp.R', '2019-10-25 13:28:17', 1571981297.2041583, 'file', '17.36kb', './tmp.R'],
            file=arr[0];
            fTime=arr[1];
            fTimeNum=arr[2];
            fType=arr[3]
            Size=arr[4]
            url=arr[5]
            #
            if fType=='file': #type="file"
                htmlF+="<tr class=file data-time='"+str(fTimeNum)+"'> <td><input type='checkbox' tabindex='-1'></td> <td>"+img['file']+" <a title='点击下载' target='_blank' href='/download?filename="+file+"&path="+fpath+"'>"+file+"</a></td>  <td>"+Size+"</td>   <td>"+fTime+"</td>  </tr>\n"
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
    
    if fname:
        t = time.strftime('%Y%m%d%H%M%S')
        new_fname = os.path.join(rootPath, uploadDir, fname.filename);
        if os.path.exists(new_fname): #如果存在，则加时间戳前缀
            new_fname = os.path.join(rootPath, uploadDir, t +'_'+ fname.filename);
        fname.save(new_fname)  #保存文件到指定路径
        url=url_for('getfiles',fpath=uploadDir );
        #return url;
        return '<meta http-equiv="refresh" content="3;url='+url+'">'+"Upload Success!. Returning to list in 3 seconds.<br>";
    else:
        return '{"msg": "上传文件不能为空！(请先选择上传文件)"}'



# 添加新静态文件的路径，这样就允许xx/下的图片加载了
@server.route("/static/<path:filename>")
def downloader(filename):
    return send_from_directory("static",filename,as_attachment=False)



# run the app
if __name__ == '__main__':
    server.debug = True # 设置调试模式，生产模式的时候要关掉debug
    env=sys.platform #"win32"测试环境;  "linux"生产环境
    print('env=',env)
    if env=='linux':
        server.run(host="192.168.2.120",port=8000) #ubuntu
    elif env=='win32':
        server.run(host="127.0.0.1",port=8005) #windows
        
        