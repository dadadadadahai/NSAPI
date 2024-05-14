from django.shortcuts import render
from . import models
from django.conf import settings
from django.http import HttpResponse
import base64,time
# Create your views here.
def index(request,uid):
    #执行验证
    userinfo = models.userinfo.objects(_id=uid).first()
    if not userinfo:
        return render(request,'index/result.html',{
            'msg':'O usuário n?o existe',
            'status':0,
        })
    if models.userImageUpload.objects(_id=uid).first():
        return render(request,'index/result.html',{
            'msg':'Carregado e compartilhado',
            'status':0,
        })
        
    if request.method == 'POST':
        file = request.FILES.get('fileToUpload')
        if file:
            filename = 'image_evaluate_%s.png'%(uid)
            savepath = '%s/image_evaluate_%s.png' % (settings.MEDIA_ROOT, uid)
            with open(savepath,'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            #保存数据库
            models.userImageUpload(_id=uid,imgData=filename,timestamp=time.time(),status=1,uploadFlag= 1).save()
            #更新数据库状态
            return render(request,'index/result.html',{
                'msg':'Upload com sucesso',
                'status':1,
            })
        else:
            return render(request,'index/result.html',{
                'msg':'Falha no upload',
                'status':0,
            })
            
    else:
        return render(request,'index/index.html',{
            'uid':uid,
        })

#是否添加到桌面或书签
def addIndex(request, uid):
    # 执行验证
    userinfo = models.userinfo.objects(_id=uid).first()
    if not userinfo:
        return render(request, 'index/result.html', {
            'msg': 'O usuário n?o existe',
            'status': 0,
        })
    if models.userImageAddDesktop.objects(_id=uid).first():
        return render(request, 'index/result.html', {
            'msg': 'Carregado e compartilhado',
            'status': 0,
        })

    if request.method == 'POST':
        file = request.FILES.get('fileToUpload')
        if file:
            filename = 'image_addApp_%s.png' % (uid)
            savepath = '%s/image_addApp_%s.png' % (settings.MEDIA_ROOT, uid)
            with open(savepath, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            # 保存数据库
            models.userImageAddDesktop(_id=uid, imgData=filename, timestamp=time.time(), status=1, uploadFlag=1).save()
            # 更新数据库状态
            return render(request, 'index/result.html', {
                'msg': 'Upload com sucesso',
                'status': 1,
            })
        else:
            return render(request, 'index/result.html', {
                'msg': 'Falha no upload',
                'status': 0,
            })

    else:
        return render(request, 'index/index.html', {
            'uid': uid,
        })