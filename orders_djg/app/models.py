from django.db import models

# Create your models here.
class User(models.Model):

    email = models.CharField(max_length=50, verbose_name="email",primary_key=True)
    userid=models.CharField(max_length=50,unique=True)
    password=models.CharField(max_length=20,)
    avatars=models.ImageField(upload_to='avatars',
                              blank=True, null=True, verbose_name='用户头像')#头像
    date=models.CharField(max_length=20,)
    introduction=models.TextField(max_length=None,null=True)#简介
    phonenumber=models.CharField(max_length=15,null=True)
    nickname=models.CharField(max_length=20,null=True)
    status=models.CharField(max_length=10,null=True)#use the field verify token

#order detail sql
class ProjectDetail(models.Model):
    email=models.CharField(max_length=50)
    orderid=models.CharField(max_length=40,primary_key=True)# 不允许重复值出现
    contentdetail=models.JSONField(null=True,verbose_name='包含了文本和文件的具体位置和内容')
    '''
    具体是一个dict:{
        text:[{index:x,uuidname:''}],file:[{uuidname:'',filename:''}]之所以要保存 原file name，because因为 have 重复的文件name
    }
    '''
    createdate=models.IntegerField(verbose_name='创建时间的时间戳')
    title=models.CharField(max_length=100,)
    money=models.FloatField(default=0.00,)
    deadline=models.IntegerField(verbose_name='期限',null=True)
    type=models.CharField(max_length=50)
    payment=models.BooleanField(verbose_name='付款情况',null=True,)
    takename=models.CharField(max_length=50,verbose_name='接单者',null=True,)
    finish=models.BooleanField(verbose_name='完成情况',null=True)
class T_FDetail(models.Model):
    nowdate=models.CharField(max_length=30,)
    email=models.CharField(max_length=50,null=True)
    uuidname=models.CharField(max_length=50,primary_key=True)
    type=models.CharField(max_length=10)
    content=models.TextField(max_length=None,null=True)
    path=models.FilePathField(path=None,null=True)
class ProjectType(models.Model):
    id=models.AutoField(primary_key=True,)
    typename=models.CharField(max_length=20)

class Message(models.Model):
    messageid=models.CharField(primary_key=True,max_length=50)
    from_user=models.CharField(max_length=50)
    to_user=models.CharField(max_length=50)
    type=models.CharField(max_length=50)
    content=models.TextField(max_length=None,null=True)
    senddate = models.IntegerField(verbose_name='创建时间的时间戳')
    uuidname = models.CharField(max_length=50, null=True,verbose_name='file_uuidname')
    unread=models.BooleanField(null=True)


class MessageFile(models.Model):
    uuid=models.CharField(primary_key=True,max_length=50)
    path=models.FilePathField(path=None)
    adddate=models.IntegerField(null=True)

class FinishOrder(models.Model):
    orderid=models.CharField(primary_key=True,max_length=50)
    t_fcontent=models.JSONField(null=True,verbose_name='包含了文本和文件的具体位置和内容')
    finish=models.BooleanField(null=True,default=False)
    commit=models.IntegerField(verbose_name='commit number',null=True)

    

'''
 # 获取一个文件管理器对象
    file = request.FILES['pic']

    # 保存文件
    new_name = getNewName('avatar') # 具体实现在自己写的uploads.py下
	# 将要保存的地址和文件名称
    where = '%s/users/%s' % (settings.MEDIA_ROOT, new_name)
    # 分块保存image
    content = file.chunks()
    with open(where, 'wb') as f:
        for i in content:
            f.write(i)

    # 上传文件名称到数据库
    User.objects.filter(name='trent').update(avatar=new_name)

'''