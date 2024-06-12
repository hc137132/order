from django.shortcuts import render,HttpResponse,get_object_or_404
from django.http import FileResponse,JsonResponse,StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.http import require_POST
import json
import base64
import time
import datetime
from django.core.mail import send_mail
import random
import sys
import uuid
from django.template.loader import get_template
from app.models import User,ProjectDetail,ProjectType,T_FDetail,Message,MessageFile,FinishOrder
import random
import os
import jwt
from app.tool.pill import Pill,SetToken,Avatars,getsql
# Create your views
from django import *


current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 当前项目文件夹D:\python库\django\orders_djg,
path = os.path.join(current_dir, r'static\files', str(datetime.date.today()))#PATH=D:\python库\django\orders_djg\static\files\2024-x-x


def test(request):
    # return render(request,'test.html')
    data={'code':'test success'}
    return JsonResponse(data)


#signup user
@csrf_exempt
def signup(request):
    if request.method=='POST':
        # 接收到formdata的出文件之外的数据
        form = request.POST
        # formdata在vue中同一个key传入了多个value，value成为了一个数组，所以需要使用getlist来获取所有文件
        # new_files = request.FILES.getlist('new_files')
        User.objects.create(email=form['email'],password=form['password'],date=form['date'],userid=form['userid'])
        print('line40',form)
        return HttpResponse(json.dumps(request.POST))
    return HttpResponse('404')
#send email otp
@csrf_exempt
def emailauth(request,):
    if request.method=='POST':
        email=request.POST.get('email')
        print(email)
        sms_code = '%06d' % random.randint(0, 999999)
        print(sms_code)
        EMAIL_FROM = "19982840632@163.com"  # 邮箱来自
        email_title = '邮箱激活'
        template = get_template('email.html')

        # 将 userid和rand_str两个参数传入 SendEmailCode1.html 文件中
        # 如果又有多个参数，可累加 即：{'userid': userid, 'rand_str': rand_str, 'key1':value1, 'key2':value2,.........}
        html_content = template.render({'code': sms_code})

        # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，
        # 收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
        # send_mail(subject=email_title,message=None,html_message=html_content ,
        #          from_email =EMAIL_FROM,recipient_list=[email],fail_silently=False)

        return HttpResponse(json.dumps({'auth':sms_code}))

    return HttpResponse('404')
#email name use
@csrf_exempt
def usernamedete(request,):
    if request.method=='POST':
        email=request.POST.get('email')
        data={'code':0,}
        email=User.objects.filter(email=email).first()
        if email:
            data['code']=1
            return HttpResponse(json.dumps(data),content_type='text/html')
        else:
            return HttpResponse(json.dumps(data))



    return HttpResponse('404')


@csrf_exempt
def robotverify(request):
    if request.method=="GET":

        pil=Pill()

        return JsonResponse(pil.xy())
@csrf_exempt
def login(request,):
    if request.method=='POST':

        email=request.POST.get('email')
        password=request.POST.get('password')
        data={'code':0}
        useremail=User.objects.filter(email=email).first()
        if useremail and password==useremail.password:
            payloads = {'user': email, 'exp': int(time.time())+3600*2}
            # 生成token
            settoken=SetToken()
            token=settoken.Encrypt(payloads)
            data['token']=token
            return JsonResponse(data)
        else:
            data['code']=1
            return JsonResponse(data)

    return HttpResponse('404')

#验证token的函数
@csrf_exempt
def verify_token(request):
    secret_key = 'hecheng'
    JWT_TOKEN_EXPIRE_TIME = int(time.time())
    if request.method=='GET':
        token=request.META['HTTP_AUTHORIZATION']# 获取前端回来的token['HTTP_AUTHORIZATION']'HTTP_TOKEN'
        # print(token,5555)
        try:   
            # 验证JWT
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            print('token',payload)
            userobj=User.objects.filter(email=payload['user']).first()
            if payload['exp'] >= JWT_TOKEN_EXPIRE_TIME and userobj.status!='N':  # 未过期,且允许登录
                print('login')
                return JsonResponse(payload)

            else:
                print('Expried')
                return HttpResponse('EXPRIED')

        except:
            print('INvalid')
            return HttpResponse('Invalid')  # 无效
    else:

        token = request.META['HTTP_AUTHORIZATION'] # 获取前端回来的token['HTTP_AUTHORIZATION']'HTTP_TOKEN'
        print(token, 5555)
        try:
            # 验证JWT
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            print(payload)
            userobj = User.objects.filter(email=payload['user']).first()
            if payload['exp'] >= JWT_TOKEN_EXPIRE_TIME and userobj.status != 'N':  # 未过期,且允许登录
                return JsonResponse(payload)
            else:
                return HttpResponse('EXPRIED')

        except:
            return HttpResponse('Invalid')  # 无效

# get user data
@csrf_exempt
def userdata(request):
    if request.method=='POST':
        userdata=None
        print(1599,request.POST.get('userid'),request.POST.get('email'))
        if request.POST.get('email'):
            # print('email')
            userdata=User.objects.filter(email=request.POST['email']).first()
        if request.POST.get('userid'):
            # print('userid')
            userdata = User.objects.filter(userid=request.POST['userid']).first()
        # print(request.META,222222)
        path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'static','avatars')#定位到orders_djg,+static+avatars
        # print(userdata,1655)
        avatar=None
        try:
            if userdata.avatars:
                file =os.path.join(path,str(userdata.avatars))
                f = open(file, 'rb')
                avatar= base64.b64encode(f.read()).decode('utf-8')
                f.close()
                # print(avatar)
            else:
                # avatar=None
                pass
        except:
            print('userdata.avatars error')

        data={
            'email':userdata.email,
            'userid':userdata.userid,
            'avatar':avatar,
            'date':userdata.date,
            'introduction':userdata.introduction,
            'phonenumber':userdata.phonenumber,
            'nickname':userdata.nickname
        }
        # print(data)
        return JsonResponse(data)

@csrf_exempt
def userupdate(request):
    path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'static','avatars')#定位到orders_djg,+static+avatars
    if request.method=='POST':
        print(request.POST)
        email=request.POST.get('email')
        dataa = {'code': 0}
        for key in ['avatar', 'introduction', 'nickname', 'phonenumber']:
            # Baoxpeople.objects.filter(number=number).update(name=name, baoxbz=baoxbz)
            try:
                data = request.POST.get(key,default=None)
                if data:
                    if key== 'avatar':
                        if data != '%Null%':
                            imgdata = base64.b64decode(data.split(',')[1])  # 将bytes to file
                            uuid_str = uuid.uuid4().hex
                            filename = uuid_str + '.jpeg'
                            # print(os.path.join(path,tmp_file_name))
                            with open(os.path.join(path, filename), 'wb') as f:  # 如果不设置path，它会shop目录文件夹下
                                f.write(imgdata)
                            User.objects.filter(email=email).update(avatars=filename)
                        elif data == '%Null%':
                            User.objects.filter(email=email).update(avatars=None)
                    elif key== 'introduction':
                        if data != '%Null%':
                            User.objects.filter(email=email).update(introduction=data)
                        elif data == '%Null%':
                            User.objects.filter(email=email).update(introduction=None)

                    elif key== 'nickname':
                        if data != '%Null%':
                            User.objects.filter(email=email).update(nickname=data)
                        elif data == '%Null%':
                            User.objects.filter(email=email).update(nickname=None)

                    elif key== 'phonenumber':
                        if data != '%Null%':
                            User.objects.filter(email=email).update(phonenumber=data)
                        elif data == '%Null%':
                            User.objects.filter(email=email).update(phonenumber=None)
                else:
                    print(key+'undefined--default')
            except:
                dataa['code']='error'

        return JsonResponse(dataa,safe=False)

@csrf_exempt
def addorder(request,takename=None,payment=False):
    if request.method=='POST':
        data={'code':1}
        try:
            if os.path.isdir(path):#检测当前文件夹是否存在，没有就创建当日文件夹，当天所有的文件存到当天文件夹
                pass
            else:
                os.mkdir(path)
            title=request.POST.get('title')
            # print('orderid',request.POST.get('orderid'))
            deadline=request.POST.get('date')
            date=0
            if deadline!='None':
                date=int(deadline)
            type=request.POST.get('type')
            createdate=request.POST.get('createdate')
            money=request.POST.get('money')
            tfdata=request.POST.get('tfdata')#str(uuid.uuid1()).replace('-','')
            ProjectDetail.objects.create(email=request.POST.get('email'),orderid=request.POST.get('orderid'),takename=takename,
                                         contentdetail=tfdata,createdate=createdate,title=title,money=money,deadline=date,type=type,finish=False,payment=payment
                                         )
            #create dict == text:[{index:x,uuidname:''}],file:[{uuidname:'',filename:''}]
            nowdate=path.split('\\')[-1]
            # print("POST_DATA", title, date, type, createdate, money, tfdata)
            for a in json.loads(tfdata)['text']:
                # print(a['uuidname'],a['index'])
                # print('TEXT',request.POST.get(a['uuidname']))
                T_FDetail.objects.create(nowdate=nowdate,email=request.POST.get('email'),uuidname=a['uuidname'],type='text',content=request.POST.get(a['uuidname']))
            for a in json.loads(tfdata)['files']:
                file=request.FILES.get(a['uuidname'])
                # print('FILE',a['uuidname'],file.name)
                savepath=path.split('\\')[-1]+'\\'+a['uuidname']#this save to mysql path,上一级文件夹是static/files
                with open(path+'\\'+a['uuidname'], 'wb+') as f:  # 写文件word
                    for chunk in file.chunks():
                        f.write(chunk)
                f.close()
                T_FDetail.objects.create(nowdate=nowdate, email=request.POST.get('email'), uuidname=a['uuidname'],
                                         type='file', path=savepath)

            print("POST_DATA",title,date,type,createdate,money,tfdata)
            return JsonResponse({'code':1})
        except IndexError as e:
            data['code']=0
            print(e)
        return JsonResponse(data)


@csrf_exempt
def getorders(request):
    if request.method=="POST":
        datalist=[]
        print(request.POST.get('email'))
        data = ProjectDetail.objects.filter(email=request.POST.get('email')).all()
        # print(data)
        for a in data:
            datalist.append({
                        'orderid':a.orderid,
                'createdate':a.createdate, 'title':a.title,
                'money':a.money,'deadline':a.deadline,'type':a.type,
                'payment':a.payment,'takename':a.takename,
                'contenydetail':a.contentdetail,'finish':a.finish
            })
        # print(datalist)
        return JsonResponse({'code': 'getorders','datalist':datalist })


@csrf_exempt
def getorderdetail(request):

    def read_file(file_name, size):
        """分批读取文件"""
        with open(file_name, mode='rb') as fp:
            while True:
                c = fp.read(size)
                if c:
                    # 生成器，相当于一个特殊的迭代器，当运行到这个语句的时候会保存当前的对象；下次再运行到这里的时候会接着上次的对象继续运行。
                    yield c
                else:
                    break
    if request.method=='POST':
        try:
            if request.POST.get('id'):
                verify_token(request)
                data=ProjectDetail.objects.filter(orderid=request.POST.get('id')).first()
                data={'email':data.email,
                        'orderid': data.orderid,
                        'createdate': data.createdate, 'title':data.title,
                        'money': data.money, 'deadline': int(data.deadline), 'type': data.type,
                        'payment': data.payment, 'takename':data.takename,
                        'contentdetail':data.contentdetail, 'finish': data.finish
                    }
                print(data)
                return JsonResponse(data)
            elif request.POST.get('t_fid'):

                data=T_FDetail.objects.filter(email=request.POST.get('email'),uuidname=request.POST.get('t_fid')).first()
                print('Line ' + str(sys._getframe().f_lineno),data,request.POST.get('email'),request.POST.get('t_fid'))
                if data.type=='text':
                    data={
                            'content':data.content
                        }
                    return JsonResponse(data)
                elif data.type=='file':

                    filename=request.POST.get('t_fid')
                    # path=T_FDetail.objects.filter(email=request.POST.get('email'),uuidname=request.POST.get('t_fid')).first()


                    # 获取文件的路径
                    current_dir = os.path.dirname(
                        os.path.dirname(os.path.abspath(__file__)))  # 当前项目文件夹D:\python库\django\orders_djg,
                    path = os.path.join(current_dir, r'static\files\\', data.path)  # 文件完整的path，包含filename

                    # 将下载文件分批次写入本地磁盘，先不将他们载入文件内存，读取文件，以512B为单位构建迭代器
                    response = StreamingHttpResponse(read_file(path, 1024))
                    response['Content-Length'] = os.path.getsize(path)
                    # 作为文件直接下载到本机，用户再用软件打开
                    response['Content-Type'] = 'application/octet-stream'
                    # 规定文件名的下载格式，在文件名为中文时，要加上escape_uri_path
                    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
                    return response
        except Exception as e:
            print(e)
            return JsonResponse({'code':'tokenlose'})
@csrf_exempt
def filedown(request):
    def read_file(file_name, size):
        """分批读取文件"""
        with open(file_name, mode='rb') as fp:
            while True:
                c = fp.read(size)
                if c:
                    # 生成器，相当于一个特殊的迭代器，当运行到这个语句的时候会保存当前的对象；下次再运行到这里的时候会接着上次的对象继续运行。
                    yield c
                else:
                    break
    if request.method=='POST':
        path=None
        filename=None
        # tihs is orders_file down
        if request.POST.get('t_fid'):
            filename = request.POST.get('t_fid')
            path = T_FDetail.objects.filter(email=request.POST.get('email'), uuidname=request.POST.get('t_fid')).first()

            # 获取文件的路径
            current_dir = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))  # 当前项目文件夹D:\python库\django\orders_djg,
            path = os.path.join(current_dir, r'static\files\\', path.path)  # 文件完整的path，包含filename
            #this is message_Filedown
        if request.POST.get('type') == 'down':
            path=MessageFile.objects.filter(uuid=request.POST.get('uuidname')).first().path
            filename=path.split('\\')[-1]
        elif request.POST.get('type')=='finish':
            path = T_FDetail.objects.filter(uuidname=request.POST.get('uuidname')).first().path
            filename = path.split('\\')[-1]
        print(path)
        # 将下载文件分批次写入本地磁盘，先不将他们载入文件内存，读取文件，以512B为单位构建迭代器
        response = StreamingHttpResponse(read_file(path, 512))
        response['Content-Length'] = os.path.getsize(path)
        # 作为文件直接下载到本机，用户再用软件打开
        response['Content-Type'] = 'application/octet-stream'
        # 规定文件名的下载格式，在文件名为中文时，要加上escape_uri_path
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response



#get all project type
@csrf_exempt
def typehandle(request):
    if request.method=='GET':
        data=[]
        for a in ProjectType.objects.all():
            data.append(a.typename)
        # print(data)
        return JsonResponse({'data':data}, safe=False)

    else:
        typen=request.POST.get('type')
        if typen=='add':
            ProjectType.objects.create(typename=request.POST.get('text'))
            return JsonResponse({'code':1})
        else:
            ProjectType.objects.filter(typename=request.POST.get('text')).delete()
            return JsonResponse({'code': 1})


@csrf_exempt
def updataorder(request):
    if request.method=='POST':
        dataa={'code':1}
        if request.POST.get('orderid'):
            try:
                data = ProjectDetail.objects.filter(orderid=request.POST.get('oldorderid'),
                                                    email=request.POST.get('email')).first()
                addorder(request,data.takename,data.payment)#add new order
                print('line 447', request.POST.get('oldorderid'), request.POST.get('orderid'))
                finish=FinishOrder.objects.filter(orderid=request.POST.get('oldorderid')).first()
                if finish:
                    FinishOrder.objects.filter(orderid=request.POST.get('oldorderid')).update(orderid=request.POST.get('orderid'))
                    print('line 450',request.POST.get('oldorderid'),request.POST.get('orderid'))
            except Exception as e:
                print(e)
                dataa['code']=0
                dataa['errormessage']=e
                return JsonResponse(dataa)
        # delet old order
        try:
            data=ProjectDetail.objects.filter(orderid=request.POST.get('oldorderid'),email=request.POST.get('email')).first()
            print('556888', request.POST.get('oldorderid'),type(data.contentdetail))
            for a in json.loads(data.contentdetail)['text']:
                print(1)
                T_FDetail.objects.filter(uuidname=a['uuidname']).delete()
            for a in json.loads(data.contentdetail)['files']:
                print(a,type(a))
                filepath=T_FDetail.objects.filter(uuidname=a['uuidname']).first()
                current_dir = os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__)))  # 当前项目文件夹D:\python库\django\orders_djg,
                path = os.path.join(current_dir, r'static\files\\', filepath.path)  # 文件完整的path，包含filename
                print(path)
                os.remove(path)
                T_FDetail.objects.filter(uuidname=a['uuidname']).delete()
            ProjectDetail.objects.filter(orderid=request.POST.get('oldorderid'), email=request.POST.get('email')).delete()
        except Exception as e:
            print('Line '+str(sys._getframe().f_lineno) ,e)
            dataa['code']=0
            # dataa['errormessage'] = e
        return JsonResponse(dataa)


@csrf_exempt
def getallorder(request):
    if request.method=='GET':
        datalist=[]
        pageS=request.POST.get('start')
        pageE=request.POST.get('end')
        data = ProjectDetail.objects.all()
        # print(data)
        for a in data:
            datalist.append({
                'orderid': a.orderid,
                'createdate': a.createdate, 'title': a.title,
                'money': a.money, 'deadline': a.deadline, 'type': a.type,
                'payment': a.payment, 'takename': a.takename,
                'contenydetail': a.contentdetail, 'finish': a.finish
            })
        # print(datalist)
        return JsonResponse({'code': 'getorders', 'datalist': datalist})
def getext(obj):
    newls = []
    n=0
    if obj['text']:
        while n<len(obj['text']) and n<2:
            print('line 499',obj['text'])
            for a in obj['text']:
                print('line 501',a)
                if int(a['index'])== n:
                    print('line 503',T_FDetail.objects.filter(uuidname=a['uuidname'],type='text').first().content)
                    newls.append({'type':'text','content':T_FDetail.objects.filter(uuidname=a['uuidname'],type='text').first().content})
            n+=1
    a=0
    while n < 2 and a<len(obj['files']):
        newls.append({'type':'file','content':obj['files'][a]['filename']})
        a+=1
        n += 1
    return newls
def getdetail(obj1):
    orderlist = []
    for a in obj1:
        # print(a.type,a.money,time.strftime("%Y-%m-%d", time.localtime(a.createdate)),time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(a.deadline)))
        orderlist.append({
            'email': a.email,
            'orderid': a.orderid,
            'createdate': a.createdate, 'title': a.title,
            'money': a.money, 'deadline': int(a.deadline), 'type': a.type,
            'payment': a.payment, 'takename': a.takename,
            'text_filename': getext(json.loads(a.contentdetail)), 'finish': a.finish
        })
    return orderlist
@csrf_exempt
def filterdata(request):
    data={
        'code':1,'page':'yes'
    }

    if request.method=='POST':
        searchdict = {
            'flag':False,
        }
        filterdict = json.loads(request.POST.get('filterdict'))
        page=int(request.POST.get('page'))
        if request.POST.get('search')=='yes':
            searchdict['flag']=True
            searchdict['stype']=request.POST.get('stype')
            searchdict['sname']=request.POST.get('sname')
            print(searchdict)

        namelist=['type','deadline','createdate','money']
        for a in namelist:
            if '全部' in filterdict[a]:
                filterdict[a]=[]
        print('line519',page,getsql(filterdict,searchdict))
        dataobject=ProjectDetail.objects.raw(getsql(filterdict,searchdict))[(page-1)*9:(page-1)*9+9]
        if len(dataobject)<9:
            data['page']='end'
        data['orderlist']=getdetail(dataobject)


        return JsonResponse(data)

@csrf_exempt
def message(request):
    if request.method=='POST':
        if request.POST.get('type')=='save':
            data=request.POST.get('data')
            # print(json.loads(data)['messageid'])
            data=json.loads(data)
        # {'messageid': '357c70e5-2bad-4ac0-940c-1004c91e657a', 'from': '83dc85ba2a594ce7bcc8877d21537805',
        #  'to': 'f38f8f333bf54dd09ae58a9f3e76e822', 'type': 'text', 'content': 'asda', 'uuidname': '', 'senddate
        #  ': 1716904386, 'unread': False}
            Message.objects.create(messageid=data['messageid'],from_user=data['from'],to_user=data['to'],type=data['type'],
                                    content=data['content'],senddate=int(data['senddate']),uuidname=data['uuidname'],unread=data['unread'])
            return JsonResponse({'code':1,'resule':'addmysqlDB'})
        else:
            ls=[]
            userid=request.POST.get('userid')
            # print(userid)
            chatdata=Message.objects.filter(to_user=userid).all()
            for a in chatdata:
                # print('line 558',a.messageid)
                ls.append({'messageid': a.messageid, 'from': a.from_user,
                 'to': a.to_user, 'type': a.type, 'content': a.content, 'uuidname': a.uuidname,
                           'senddate': a.senddate, 'unread': False})
            # print(ls)
            Message.objects.filter(to_user=userid).delete()
            return JsonResponse({'code':0,'chatls':ls})



@csrf_exempt
def messagefile(request):
    if request.method=='POST':
        current_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))  # 当前项目文件夹D:\python库\django\orders_djg,
        path = os.path.join(current_dir, r'static\files', str(datetime.date.today()))  # 要存到的文件夹
        if os.path.isdir(path):  # 检测当前文件夹是否存在，没有就创建当日文件夹，当天所有的文件存到当天文件夹
            pass
        else:
            os.mkdir(path)
        if request.POST.get('type')=='up':
            file=request.FILES.get('file')
            uid=request.POST.get('uuidname')
            pathname = path+'\\'+uid# this save to mysql path,上一级文件夹是static/files,
            print('line548',pathname,uid)
            with open(pathname, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            f.close()
            MessageFile.objects.create(uuid=uid,path=pathname,adddate=request.POST.get('adddate'))
            return JsonResponse({'code': 1})
    return JsonResponse({'code': 1})

@csrf_exempt
def receiveorder(request):
    if request.method=='POST':
        userid=request.POST.get('userid')
        orderid=request.POST.get('orderid')
        vertify=ProjectDetail.objects.filter(orderid=orderid).first()
        if vertify.takename:
            return JsonResponse({'code':0,'res':'exists'})
        else:
            ProjectDetail.objects.filter(orderid=orderid).update(takename=userid)
        # 返回my task all orderid
            return JsonResponse({'code':1,'res':'success'})

@csrf_exempt
def mytask(request):
    if request.method=='POST':
        userid=request.POST.get('userid')
        orders=ProjectDetail.objects.filter(takename=userid).all()
        # 返回my task all orderid
        ls = getdetail(orders)

        return JsonResponse({'code':1,'orders':ls})

@csrf_exempt
def orderfinish(request):
    if os.path.isdir(path):  # 检测当前文件夹是否存在，没有就创建当日文件夹，当天所有的文件存到当天文件夹
        pass
    else:
        os.mkdir(path)
    # 要存到的文件夹
    if request.method=='POST':
        orderid = request.POST.get('id')
        type1=request.POST.get('type')

        order = FinishOrder.objects.filter(orderid=orderid).first()
        print('line639',type1, order,orderid)
        if type1=='get':
            if order:
                return JsonResponse({'data':json.dumps(order.t_fcontent),'finish':order.finish})
            else:
                return JsonResponse({ 'finish': False})
        elif type1 == 'update' or (type1 =='delete' and order!=None):
            print('line646',type(order),order)
            if order.t_fcontent['text']:
                T_FDetail.objects.filter(uuidname=order.t_fcontent['text']).delete()
            for a in order.t_fcontent['files']:
                pathname=T_FDetail.objects.filter(uuidname=a['uuidname']).first()
                if os.path.exists(pathname.path):
                    os.remove(pathname.path)
                T_FDetail.objects.filter(uuidname=a['uuidname']).delete()
            FinishOrder.objects.filter(orderid=orderid).delete()
        if type1=='delete':
            ProjectDetail.objects.filter(orderid=orderid).update(takename=None)
            return JsonResponse({'code':'order delete success'})
        detail = json.loads(request.POST.get('orderjson'))

        finish=request.POST.get('finish')
        if finish=='false':
            finish=False
        else:
            finish=True
        FinishOrder.objects.create(orderid=orderid,t_fcontent=detail,commit=1,finish=finish)
        print('line 665' ,detail)
        if detail['text']:
            T_FDetail.objects.create(nowdate=datetime.date.today(), uuidname=detail['text'],
                                     type='text', content=request.POST.get(detail['text']))
        if len(detail['files'])>0:
            for a in detail['files']:
                file = request.FILES.get(a['uuidname'])
                # print('FILE',a['uuidname'],file.name)
                savepath = path + '\\' + a['uuidname']  # this save to mysql path,上一级文件夹是static/files
                with open(savepath, 'wb+') as f:  # 写文件word
                    for chunk in file.chunks():
                        f.write(chunk)
                f.close()
                T_FDetail.objects.create(nowdate=datetime.date.today(), uuidname=a['uuidname'],
                                         type='file', path=savepath)

        return JsonResponse({'code':1})

@csrf_exempt
def payment(request):
    if request.method=='POST':
        orderid=request.POST.get('orderid')
        userid=request.POST.get('userid')
        print(orderid,userid)
        # 配置支付宝客户端
        # alipay = AliPay(
        #     appid="your_app_id",#支付宝分配给你的应用 ID。可以在支付宝开放平台的应用管理页面找到。
        #     app_notify_url=None,  # 默认回调 url用于接收支付宝的支付结果通知。如果不设置，则使用订单生成时指定的 notify_url。
        #     app_private_key_path=os.path.join("path_to_your_private_key.pem"),#应用私钥的文件路径。用于对请求进行签名。
        #     alipay_public_key_path=os.path.join("path_to_alipay_public_key.pem"),#支付宝公钥的文件路径。用于验证支付宝返回结果的签名。
        #     sign_type="RSA2",
        #     debug=True  # 沙箱环境
        # )

        # 生成订单信息
        # order_string = alipay.api_alipay_trade_page_pay(
        #     out_trade_no=orderid, # 商户订单号，需要保证唯一性
        #     total_amount="100.00", # 订单总金额，单位为元
        #     subject="Order {}".format(orderid),# 订单标题
        #     return_url="https://your_domain.com/paymentresult", # 用户付款成功后跳转的页面
        #     notify_url="https://your_domain.com/paymentresult"# 支付结果通知的 URL
        # )
        #
        # payment_url = "https://openapi.alipaydev.com/gateway.do?" + order_string
        # qr_code_url = "https://openapi.alipaydev.com/gateway.do?" + order_string  # 示例，仅用于说明
        #
        response_data = {
            'paymentUrl':' payment_url',
            'qrCodeUrl': 'qr_code_url'
        }

        return JsonResponse(response_data)


@require_POST
@csrf_exempt
def payment_notify(request):
    # 配置支付宝客户端
    # alipay = AliPay(
    #     appid="your_app_id",
    #     app_notify_url=None,  # 默认回调 url用于接收支付宝的支付结果通知。如果不设置，则使用订单生成时指定的 notify_url。
    #     app_private_key_path=os.path.join("path_to_your_private_key.pem"),  # 应用私钥的文件路径。用于对请求进行签名。
    #     alipay_public_key_path=os.path.join("path_to_alipay_public_key.pem"),  # 支付宝公钥的文件路径。用于验证支付宝返回结果的签名。
    #     sign_type="RSA2",
    #     debug=True  # 沙箱环境
    # )

    data = request.POST.dict()
    signature = data.pop("sign")

    # success = alipay.verify(data, signature)

    # if success:
    #     order_id = data.get('out_trade_no')
    #     channel_layer = get_channel_layer()
    #     async_to_sync(channel_layer.group_send)(
    #         f'order_{order_id}',
    #         {
    #             'type': 'send_payment_status',
    #             'message': 'success'
    #         }
    #     )
    #     return HttpResponse("success")
    # else:
    #     return HttpResponse("failure")
    return HttpResponse("failure")

@csrf_exempt
def gettext(request):
    if request.method=="POST":
        print(request.POST.get('uuid'))
        text=T_FDetail.objects.filter(uuidname=request.POST.get('uuid')).first()
        return HttpResponse(text.content)


@csrf_exempt
def surefinish(request):
    if request.method=='POST':
        orderid=request.POST.get('id')
        ProjectDetail.objects.filter(orderid=orderid).update(finish=True)
        return JsonResponse({'data':1})

@csrf_exempt
def repwd(request):
    if request.method=='POST':
        userid=request.POST.get('userid')
        pwd=request.POST.get('pwd')
        newpwd=request.POST.get('newpwd')
        data=User.objects.filter(userid=userid).first()
        if data.password==pwd:
            User.objects.filter(userid=userid).update(password=newpwd)
            return JsonResponse({'code': 'success'})
        else:
            return JsonResponse({'coed':'pwderror'})

