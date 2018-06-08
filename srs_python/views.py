#coding:utf-8
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response
from urllib2 import urlopen
import json
from django.contrib.auth.models import User
import json
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import getsysinfo
import os
import time
from django.template.loader import get_template
from django import forms
import shutil
# Create your views here.

def getData(request):
    url = 'http://192.168.218.124:1985/api/v1/summaries'
    rawtext = urlopen(url,timeout=15).read()
    jsonStr = json.loads(rawtext)
    json_self = jsonStr[u'data'][u'self']
    json_sys = jsonStr[u'data'][u'system']
    return render(request, 'srs_view.html',{'json_self':json_self.item})
                  # {
                  #                       #self
                  #                       'version':json_self['version'],
                  #                       'pid': json_self['pid'],
                  #                       'argv':json_self['argv'],
                  #                       'mem_kbyte':json_self['mem_kbyte'],
                  #                       'cpu_percent':json_self['cpu_percent'],
                  #                       'srs_uptime':json_self['srs_uptime'],
                  #                       #system
                  #                       'sys_cpu_percent':json_sys['cpu_percent'],
                  #                       'disk_read_BKps':json_sys['disk_read_KBps'],
                  #                       'disk_write_KBps':json_sys['disk_write_KBps'],
                  #                       'disk_busy_percent':json_sys['disk_busy_percent'],
                  #                       'mem_ram_kbyte':json_sys['mem_ram_kbyte'],
                  #                       'mem_ram_percent':json_sys['mem_ram_percent'],
                  #                       'mem_swap_kbyte':json_sys['mem_swap_kbyte'],
                  #                       'mem_swap_percent':json_sys['mem_swap_percent'],
                  #                       'cpus':json_sys['cpus'],
                  #                       'cpus_online':json_sys['cpus_online'],
                  #                       'uptime':json_sys['uptime'],
                  #                       'ilde_time':json_sys['ilde_time'],
                  #                       'load_1m':json_sys['load_1m'],
                  #                       'load_5m':json_sys['load_5m'],
                  #                       'load_15m':json_sys['load_15m'],
                  #                       'net_sample_time':json_sys['net_sample_time'],
                  #                       'net_recv_bytes':json_sys['net_recv_bytes'],
                  #                       'net_send_bytes':json_sys['net_send_bytes'],
                  #                       'net_recvi_bytes':json_sys['net_recvi_bytes'],
                  #                       'net_sendi_bytes':json_sys['net_sendi_bytes'],
                  #                       'srs_sample_time':json_sys['srs_sample_time'],
                  #                       'srs_recv_bytes':json_sys['srs_recv_bytes'],
                  #                       'srs_send_bytes':json_sys['srs_send_bytes'],
                  #                       'conn_sys':json_sys['conn_sys'],
                  #                       'conn_sys_et':json_sys['conn_sys_et'],
                  #                       'conn_sys_tw':json_sys['conn_sys_tw'],
                  #                       'conn_sys_udp':json_sys['conn_sys_udp'],
                  #                       'conn_srs':json_sys['conn_srs']
                  #                       })

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
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            #必须使用create_user，不能使用create
            User.objects.create_user(username=username,password=password)

            return HttpResponse('注册成功')
    else:
        userform = UserForm()
    return render(request,'regist.html',{'userform':userform})

def log_in(request):
    next = request.GET.get('next', '/')
    if request.method == 'POST':
        userform = UserForm(request.POST)
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
                return render(request, 'login.html', {'userform': userform,'error':'用户名或密码错误，请重新登陆'})
    else:
        userform = UserForm()
    return render(request,'login.html',{'userform':userform,'next':next})

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