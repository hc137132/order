import json
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
from channels.exceptions import StopConsumer
from channels.layers import get_channel_layer
import redis
import asyncio
import json
from asgiref.sync import async_to_sync,sync_to_async


r = redis.Redis(host='localhost', port=6379, db=0)

class ChatConsumer(WebsocketConsumer):
    def connect(self):#接收客服端连接
        self.accept()#允许连接
        print('connect success',)
        # get url argument==群号username
        username=self.scope['url_route']['kwargs']['username']
        print('line17',username,self.channel_name)
        # 将连接者obj加入到USER_LIST or channels_layers
        # print(self.channel_name)
        async_to_sync(self.channel_layer.group_add)(username,self.channel_name)#第二个参数是当前创建者

        # 发送新加入的用户信息给所有在线用户
        # async_to_sync(self.channel_layer.group_send)(username,{'type': 'user_joined',  'username': username })
        # 将用户标记为在线（这里使用Redis的集合），以便发送消息时检测用户是否在线
        # r.sadd('online_users', username)

        r.set(username,'online')
        print(username,' join redis')
        # 将用户名和通道名称存储在Redis哈希中
        # r.hset('user_channels', username, self.channel_name)

        # 接收客户端的消息
    def websocket_receive(self,message):

        # print('接收--->', message)
        # json1 = json.loads(str1)
        # self.send(str1)  # 返回给客户端的消息
        username = self.scope['url_route']['kwargs']['username']
        # 收到的消息格式
        '''
        message={from:username,to:username,type:text/file,
        content:'text'/filename.png,
        uuidname:'sdasdj.png'
        }
        '''
        # 接收到前端的message
        # type=vretify时,send-user,并r.delete(username)

        # 前端如何在线返回 type=result,r.set(username)

        user=json.loads(message['text'])['to']
        print('line48',user)
        # r.flushdb()
        status=r.exists(user)

        # my=r.exists(json.loads(message['text'])['from'])
        print('line55',status)
        # 发向对方的消息
        if status:
            # 使用Channels的send方法发送消息给特定用户的通道
            channel_layer = get_channel_layer()
            print(user)
            async_to_sync(self.channel_layer.group_send)(user,{'type':'method','message':message})
            # async_to_sync(channel_layer.send)(user, {'type': 'websocket.receive', 'text':message})
        else:
            # 用户不在线，处理这种情况（例如记录日志或发送通知）

            print(f"User {user} is not online.",json.loads(message['text'])['from'])
            async_to_sync(self.channel_layer.group_send)(json.loads(message['text'])['from'], {'type': 'method', 'message':message})
            # 第一个参数是转发到哪个群，{第一个是执行一个method函数，第二个是传递的message}ssss
        # async_to_sync(self.channel_layer.group_send)('bbb',{'type':'method','message':message})
    def method(self,message):
        # print(message)
        self.send(message['message']['text'])#发给当前group里的所有人
    def disconnect(self, message):#与server断开时执行
        print('stop__',message)
        # self.close()#主动关闭
        print(self.channel_name,'exit')
        username = self.scope['url_route']['kwargs']['username']
        async_to_sync(self.channel_layer.group_discard)(username,self.channel_name)
        r.delete(username)
        # self.channel_layer.group_discard(username, self.channel_name)
        raise StopConsumer()


        # 处理用户加入事件
    def user_joined(self, event):
        username = event['username']
        # 这里可以发送一个消息给前端，告知新用户已加入
        # self.send(text_data=f"User {username} joined the chat.")
    # 处理用户退出事件
    def user_left(self, event):
        username = event['username']
        # 这里可以发送一个消息给前端，告知用户已退出
        # self.send(text_data=f"User {username} left the chat.")

    # def delete_group_if_empty(self, group_name):
        # group_info = self.channel_layer.group_send( group_name,{'type': 'group_info',})


class PaymentConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.group_name = f'order_{self.order_id}'

        # 加入订单组
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(self.group_name, {'type': 'send_payment_status', 'message': 'contact success'})
    def disconnect(self, close_code):
        # 离开订单组
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def websocket_receive(self,message):

        pass

    def send_payment_status(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))

