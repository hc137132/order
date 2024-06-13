import json
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
from channels.exceptions import StopConsumer
from channels.layers import get_channel_layer
import redis
import json
from asgiref.sync import async_to_sync,sync_to_async


r = redis.Redis(host='localhost', port=6379, db=0)

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        username=self.scope['url_route']['kwargs']['username']
        async_to_sync(self.channel_layer.group_add)(username,self.channel_name)
        r.set(username,'online')
    def websocket_receive(self,message):

        username = self.scope['url_route']['kwargs']['username']
        '''
        message={from:username,to:username,type:text/file,
        content:'text'/filename.png,
        uuidname:'sdasdj.png'
        }
        '''
        user=json.loads(message['text'])['to']
        status=r.exists(user)

        if status:
            channel_layer = get_channel_layer()
            async_to_sync(self.channel_layer.group_send)(user,{'type':'method','message':message})
        else:

            async_to_sync(self.channel_layer.group_send)(json.loads(message['text'])['from'], {'type': 'method', 'message':message})
    def method(self,message):
        self.send(message['message']['text'])
    def disconnect(self, message):
        print('stop__',message)
        print(self.channel_name,'exit')
        username = self.scope['url_route']['kwargs']['username']
        async_to_sync(self.channel_layer.group_discard)(username,self.channel_name)
        r.delete(username)
        raise StopConsumer()


    def user_joined(self, event):
        username = event['username']
    def user_left(self, event):
        username = event['username']


class PaymentConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.group_name = f'order_{self.order_id}'

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(self.group_name, {'type': 'send_payment_status', 'message': 'contact success'})
    def disconnect(self, close_code):
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

