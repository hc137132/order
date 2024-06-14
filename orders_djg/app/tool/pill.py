import io
from PIL import Image,ImageDraw,ImageFont
import os
import base64
import random
import jwt
import time
import re


class Pill():

    def xy(self):

        # image = Image.new(mode="RGB", size=(280, 180), color="white")
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        # print(current_dir)
        filePath = current_dir+'/static/verifyimg'
        # print(len(os.listdir(filePath)))
        imagepath=filePath+'/'+os.listdir(filePath)[random.randint(0,len(os.listdir(filePath))-1)]

        image=Image.open(imagepath)
        imgByteArr = io.BytesIO()
        # add text
        draw = ImageDraw.Draw(image)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # print(current_dir)
        current_dir.replace('\\','/')
        # print(current_dir)
        font1 = ImageFont.truetype(font=current_dir+'/刘德华字体叶根友仿版.ttf',
                                  size=random.randint(20, 30))
        font2 = ImageFont.truetype(font=current_dir+'/刘德华字体叶根友仿版.ttf',
                                  size=random.randint(20, 30))
        font3 = ImageFont.truetype(font=current_dir + '/刘德华字体叶根友仿版.ttf',
                                  size=random.randint(20, 30))
        font4 = ImageFont.truetype(font=current_dir + '/刘德华字体叶根友仿版.ttf',
                                  size=random.randint(20, 30))

        # random xy (280/4,180/4)
        textstr='可以未引入的包字比如上边的比较复杂每次使用都要用这么长的名字样本或集合中随机抽取不重复的元素形成新的序列' \
                '所以可以使用定义一个简单的名称但是使用后前边的模块名就不再起作用了'

        index=random.sample(range(len(textstr)-1), k=4)
        text=[textstr[index[0]],textstr[index[1]],textstr[index[2]],textstr[index[3]]]
        Ax, Ay = random.randint(10, 70), random.randint(20, 150)
        Bx, By = random.randint(70, 140), random.randint(20, 150)
        Cx, Cy = random.randint(140, 210), random.randint(20, 150)
        Dx, Dy = random.randint(210, 260), random.randint(20, 150)
        Ta = random.randint(0, 2)

        draw.text(xy=(Ax, Ay), text=text[0],
                  fill=(random.randint(20, 255), random.randint(20, 255), random.randint(0, 255)), font=font1)
        draw.text(xy=(Bx, By), text=text[1],
                  fill=(random.randint(20, 255), random.randint(20, 255), random.randint(0, 255)), font=font2)
        draw.text(xy=(Cx, Cy), text=text[2],
                  fill=(random.randint(20, 255), random.randint(20, 255), random.randint(0, 255)), font=font3)
        draw.text(xy=(Dx, Dy), text=text[3],
                  fill=(random.randint(20, 255), random.randint(20, 255), random.randint(0, 255)), font=font4)

        # 将图片数据编码为Base64字符串
        image.save(imgByteArr, format='JPEG')
        imgByteArr = imgByteArr.getvalue()

        image_base64 = base64.b64encode(imgByteArr).decode('utf-8')
        data={
            "text":text,
            'position':[[Ax,Ay],[Bx,By],[Cx,Cy],[Dx,Dy]],
            'image_data':image_base64
        }
        return data

class SetToken():

    def __init__(self):
        self.secret_key = 'hecheng'
        self.JWT_TOKEN_EXPIRE_TIME =int(time.time())

    def Encrypt(self,value):
        data = jwt.encode(value, self.secret_key, algorithm='HS256')

        return data

    def Decrypt(self,value):

        data = jwt.decode(value, self.secret_key, algorithms=['HS256'])
        return data

    def Veri_Token(self,value):
        try:
            # 验证JWT
            payload = jwt.decode(value,self.secret_key, algorithms=['HS256'])

            if payload['exp']>=self.JWT_TOKEN_EXPIRE_TIME :
                return payload
            else:
                return 'EXPRIED'

        except:
            return 'Invalid'

class Avatars():
    def avatars(self):
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        # print(current_dir)
        filePath = current_dir + '/static/verifyimg'
        # print(len(os.listdir(filePath)))
        imagepath = filePath + '/' + os.listdir(filePath)[random.randint(0, len(os.listdir(filePath)) - 1)]

        f=open(imagepath,'rb')
        image_base64 = base64.b64encode(f.read()).decode('utf-8')

        return image_base64

def getsql(filterdict,searchdict):
    searchsql=''
    if searchdict['flag']==True and searchdict['stype']=='主题':
        print('title')
        searchsql='(instr(title,"{}")>0) and '.format(searchdict['sname'])
    elif searchdict['flag']==True and searchdict['stype']=='用户':
        searchsql = '(instr(email,"{}")>0) and '.format(searchdict['sname'])
        print('username')
    print()
    sql = 'select * from app_projectdetail where (finish is null or finish = FALSE) and ( takename is null) and '+searchsql+'+ - @ /;'
    # print(searchsql,'---',sql)
    if filterdict['type']:
        if len(filterdict['type'])==1:
            sql=sql.split('+')[0] + 'type in ( "{}" )'.format(filterdict['type'][0]) + sql.split('+')[1]
        else:
            sql = sql.split('+')[0] + 'type in {}'.format(tuple(filterdict['type'])) + sql.split('+')[1]
        # print(sql)
    else:
        sql = 'select * from app_projectdetail where (finish is null or finish = FALSE) and ( takename is null) and '+searchsql+'type is not null - @ /;'
    onedaytime = 86400

    nowtime = int(time.time())

    header = sql.split('-')[0]
    end = sql.split('-')[1]
    if filterdict['deadline']:

        n = 0
        deadlinesyn = ''
        for a in filterdict['deadline']:
            if n == 0:
                n += 1
                if a.count('-') == 1:
                    gt = nowtime + onedaytime * int(
                        a.split('-')[0])
                    lt = nowtime + onedaytime * int(re.findall(r'\d+', a.split('-')[1])[0])
                    deadlinesyn = deadlinesyn + 'deadline between {b} and {a}'.format(a=gt, b=lt)  #
                elif a == '7天以下':
                    gt = nowtime + onedaytime * 7
                    deadlinesyn = deadlinesyn + 'deadline between 200 and {a}'.format(a=gt)
                elif a == '商议':

                    deadlinesyn = deadlinesyn + 'deadline <= 200'
                elif a == '30天以上':
                    gt = nowtime + onedaytime * 30
                    deadlinesyn = deadlinesyn + 'deadline >= {a}'.format(a=gt, )

            else:
                if a.count('-') == 1:
                    gt = nowtime + onedaytime * int(
                        a.split('-')[0])  #
                    lt = nowtime + onedaytime * int(re.findall(r'\d+', a.split('-')[1])[0])
                    deadlinesyn = deadlinesyn + ' or deadline between {b} and {a}'.format(a=gt, b=lt)
                    # print(sql, n)
                elif a == '7天以下':
                    gt = nowtime + onedaytime * 7
                    deadlinesyn = deadlinesyn + ' or deadline between 200 and {a}'.format(a=gt)
                elif a == '商议':

                    deadlinesyn = deadlinesyn + ' or deadline <= 200'
                elif a == '30天以上':
                    gt = nowtime + onedaytime * 30
                    deadlinesyn = deadlinesyn + ' or deadline >= {a}'.format(a=gt, )

        sql = header + 'and ( ' + deadlinesyn + ' )' + end
    else:
        sql = header + 'and deadline is not null' + end
    header = sql.split('@')[0]
    end = sql.split('@')[1]
    if filterdict['createdate']:
        n = 0
        createdatesyn = ''
        for a in filterdict['createdate']:
            if n == 0:
                n += 1
                if a.count('-') == 1:  # first add sql where,前面+and
                    gt = nowtime - onedaytime * int(
                        a.split('-')[0])
                    lt = nowtime - onedaytime * int(re.findall(r'\d+', a.split('-')[1])[0])
                    createdatesyn = createdatesyn + 'createdate between {a} and {b}'.format(a=gt,
                                                                                            b=lt)
                elif a == '7天以下':
                    gt = nowtime - onedaytime * 7
                    createdatesyn = createdatesyn + 'createdate >= {a}'.format(a=gt)

                elif a == '30天以上':
                    gt = nowtime - onedaytime * 30
                    createdatesyn = createdatesyn + 'createdate <= {a}'.format(a=gt, )

            else:  # second header add or
                if a.count('-') == 1:
                    gt = nowtime - onedaytime * int(
                        a.split('-')[0])
                    lt = nowtime - onedaytime * int(
                        re.findall(r'\d+', a.split('-')[1])[0])
                    createdatesyn = createdatesyn + ' or createdate between {a} and {b}'.format(a=gt, b=lt)

                elif a == '7天以下':
                    gt = nowtime - onedaytime * 7
                    createdatesyn = createdatesyn + ' or createdate >={a}'.format(a=gt)
                elif a == '30天以上':
                    gt = nowtime - onedaytime * 30
                    createdatesyn = createdatesyn + ' or createdate <= {a}'.format(a=gt, )

        sql = header + 'and ( ' + createdatesyn + ' )' + end
    else:
        sql = header + 'and createdate is not null ' + end

    header = sql.split('/')[0]
    end = sql.split('/')[1]
    if filterdict['money']:
        n = 0
        moneysyn = ''
        for a in filterdict['money']:
            # print(a)
            if n == 0:
                n += 1
                if a.count('-') == 1:
                    gt = int(a.split('-')[0])
                    lt = int( re.findall(r'\d+', a.split('-')[1])[0])
                    moneysyn = moneysyn + 'money between {b} and {a}'.format(a=gt, b=lt)  # start dont gt end
                elif a == '商议':
                    gt = nowtime - onedaytime * 7
                    moneysyn = moneysyn + 'money = 0'
                elif a == '5000元以上':
                    moneysyn = moneysyn + 'money >= 5000'
                elif a == '1000元以下':
                    moneysyn = moneysyn + 'money <= 1000'

            else:  # second header add or
                if a.count('-') == 1:
                    gt = int(a.split('-')[0])
                    lt = int( re.findall(r'\d+', a.split('-')[1])[0])
                    moneysyn = moneysyn + ' or money between {b} and {a}'.format(a=gt, b=lt)

                elif a == '商议':
                    moneysyn = moneysyn + ' or money = 0'
                elif a == '5000元以上':
                    moneysyn = moneysyn + ' or money >= 5000'
                elif a == '1000元以下':
                    moneysyn = moneysyn + ' or money <= 1000'

        sql = header + 'and ( ' + moneysyn + ' )' + end
    else:
        sql = header + ';'


    sql=re.sub(r'\s+(?=;$)', '', sql)
    return sql.split(';')[0]+' ORDER BY createdate DESC;'

