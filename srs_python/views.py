#coding:utf-8
from __future__ import unicode_literals

import shutil
import os
import time
from django.shortcuts import render,render_to_response
from urllib2 import urlopen
from django.contrib.auth.models import User
import json
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.template.loader import get_template
from django.template import RequestContext
from django import forms
import getsysinfo
import randomCode
# Create your views here.

def getData(request):
    url = 'http://192.168.218.124:1985/api/v1/summaries'
    rawtext = urlopen(url,timeout=15).read()
    jsonStr = json.loads(rawtext)
    json_self = jsonStr[u'data'][u'self']
    json_sys = jsonStr[u'data'][u'system']
    return render(request, 'srs_view.html',{'json_self':json_self.item})

def get_sys_info(request):
    data = getsysinfo.collect_monitor_data()
    # return render(request,'test.html',{'cpu_percent':data['cpu_percent']})
    return JsonResponse(data)

def get_sys_info2(request):
    data1 = getsysinfo.collect_monitor_data()
    return JsonResponse(data1,safe=False)

@login_required
def index(request):
    username = request.COOKIES.get('username','')
    data = getsysinfo.collect_monitor_data()
    return render(request,'index.html',{'data':data,'username':username})

class UserForm(forms.Form):
    username = forms.CharField(label="账号",max_length=50)
    password = forms.CharField(label="密码",widget=forms.PasswordInput())



def regist(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        username = request.POST.get('username','')
        filterResult = User.objects.filter(username=username)
        if len(filterResult) > 0:
            result = "用户名已存在"
            return JsonResponse({'result': result})
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            #必须使用create_user，不能使用create

            User.objects.create_user(username=username,password=password)
            user = authenticate(username=username, password=password)
            login(request, user)
            response = HttpResponseRedirect('/jump/')
            response.set_cookie('username', username, 3600)
            return response
    return render(request,'regist.html')


def log_in(request):
    next = request.GET.get('next', '/')
    #生成随机验证码
    verify_code_image = randomCode.randomCode()
    verify_code_image.main()
    verify_code_image_key=verify_code_image.name
    verify_code_image_value=verify_code_image.key
    cache.set(verify_code_image_key,verify_code_image_value,30)

    if request.method == 'POST':
        userform = UserForm(request.POST)
        #从POST中获取用户提交的验证码
        verify_code = request.POST.get('verify_code','')
        #从POST中获取验证码的verify_code_image_key也就是image_name
        cache_key = request.POST.get('verify_code_image_key', '')
        #从缓存中获得key为verify_code_image_key的value
        cache_value = cache.get(cache_key)
        if verify_code != cache_value:
            return render(request, 'login.html', {'error': '验证码错误', 'image_name': verify_code_image_key})
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            # user = User.objects.filter(username__exact=username,password__exact=password)
            user = authenticate(username=username,password=password)
            if user:
                login(request, user)
                if len(next)==0:
                    response = HttpResponseRedirect(next)
                else:
                    response = HttpResponseRedirect('/home/')
                response.set_cookie('username',username,3600)
                return response
            else:
                return render(request, 'login.html', {'error':'用户名或密码错误，请重新登陆','image_name':verify_code_image_key})
    return render(request,'login.html',{'next':next,'image_name':verify_code_image_key})

def log_out(request):
     logout(request)
     response = HttpResponseRedirect('/login/')
     response.delete_cookie('username')
     return response


class file():
    def __init__(self,name,size,mtime,type):
        self.name = name
        self.size = size
        self.mtime= mtime
        self.type = type

def object(request):
    path = 'C:\\Users\Administrator\Desktop\srs_admin'
    file_list = os.listdir(path)
    os.chdir(path)
    file1 = {}
    for i in file_list:
        if os.path.isdir(i):
            type = 'directory'
        else:
            type = os.path.splitext(i)[1]
        name = i
        size = os.path.getsize(i)
        mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(i)))

        file1[i] = file(name, size, mtime, type)
    file1['now_path'] = path
    return render(request,'object.html',{'file':file1})

@login_required
def files(request,path='C:/Users/Administrator/Desktop/srs_admin/'):
    username = request.COOKIES.get('username', '')
    filelist=os.listdir(path)
    os.chdir(path)
    file1={}
    for i in filelist:
        if os.path.isdir(i):
            type='directory'
        else:
            type=os.path.splitext(i)[1]
        name = i
        size = os.path.getsize(i)
        mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(i)))

        file1[i] = file(name, size, mtime, type)
    file1['now_path']=os.getcwd()
    return render(request,'files.html',{'file':file1,'username':username})


def file_table_html(request):
    if request.method == 'POST':
        path = request.POST.get('new_path','')
    filelist = os.listdir(path)
    os.chdir(path)
    file1 = {}
    for i in filelist:
        if os.path.isdir(i):
            type='directory'
        else:
            type=os.path.splitext(i)[1]
        name = i
        size = os.path.getsize(i)
        mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(i)))

        file1[i] = file(name, size, mtime, type)
    file1['now_path'] = os.getcwd().decode('gbk')
    if request.is_ajax():
        t = get_template('files_tb.html')
        content_html = t.render({'file':file1})
        playload={
            'content_html':content_html
        }
        return JsonResponse(playload)

def file_rename(request):
    if request.method == 'POST':
        file_name = request.POST.get('file_name','')
        new_name = request.POST['new_name']
    if os.path.exists(file_name) :
        if not os.path.exists(new_name):
            os.rename(file_name,new_name)
            file_info={'result':'成功重命名'}
        else:
            file_info={'result':'已经有重名的文件了'}
    else:
        file_info={'result':'重命名的源文件不存在'}
    return JsonResponse(file_info)

def file_del(request):
    if request.method == 'POST':
        file_name = request.POST.getlist('file_name[]','')
    del_num = 0
    fail_num = 0
    if len(file_name)==1:
        code=1
    else:
        code=2
    while len(file_name)!=0:
        if os.path.exists(file_name[0]):
            if os.path.isdir(file_name[0]):
                shutil.rmtree(file_name[0])
            else:
                os.remove(file_name[0])
            del_num+=1
        else:
            fail_num+=1
        file_name=file_name[1:]
    if code==1 and del_num==1:
        file_info={'result':'删除成功'}
    elif code==1 and fail_num==1:
        file_info={'result':'文件不存在，删除失败'}
    elif code==2 and fail_num==0:
        file_info = {'result': '成功删除%d个文件'%del_num}
    elif code==2 and fail_num!=0:
        file_info = {'result': '成功删除%d个文件,无法删除%d个文件，因为文件不存在' % (del_num,fail_num)}
    return JsonResponse(file_info)

def create(request):
    return render(request,'create.html')

def create_(request):
    if request.method == 'POST':
        file_type = request.POST.get('file_type','')
        new_name = request.POST.get('new_name','')
        now_path = request.POST.get('now_path','')
    if file_type=='directory':
        if  not os.path.exists(now_path+'\\'+new_name):
            os.mkdir(now_path+'\\'+new_name)
            file_info = {'result':'创建成功'}
        else:
            file_info = {'result': '创建失败，已有同名目录'}
    elif file_type=='file':
        if not os.path.exists(now_path + '\\' + new_name):
            with open(now_path + '\\' + new_name,'w') as f:
                pass
            file_info = {'result': '创建成功'}
        else:
            file_info = {'result': '创建失败，已有同名文件'}
    return JsonResponse(file_info,content_type='json')
    # return render(request,'create.html',{'file_info':file_info})

def upload_ajax(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        with open('%s'%file_obj.name,'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        file_info = {'result':"上传成功"}
        return JsonResponse(file_info,content_type='json')

def jump(request):
    return render(request,'jump.html')