# This is an order management system based on vue3 and python-django, while using mysql, indexDB, redis, it can achieve user management, order management and real-time chat, can be used for users to publish problem rewards (including text and files), Other users accept the order, solve the problem and submit relevant texts and documents according to the requirements. The publisher can view the solution submitted by the other party after paying the reward amount, and the reward amount is transferred to the other party's account after the publisher confirms that the problem is solved.

Some of the functions of this system are not perfect, the front-end page effect needs to be beautified, the code execution efficiency is poor, and the error handling needs to be improved. At present, I don't want to write it anymore, because it is too common. I hope it is useful to you.

Until then, please download and install redis yourself, as well as a browser version that supports indexDB,

### Front-end project start 
cd/orders_vue,

npm install

npm run serve

### Back-end project startup cd/orders_djg,

setting.py

line138 Email configuration

Start Redis

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrete

python manage.py runserver,



### User management module

There are login, registration, forget password, modify personal information, mailbox verification, man-machine verification, Python pillow realizes the generation of human-machine verification picture information, the front-end realizes click verification, you can modify into sliding, graphics, etc., the user will receive the back-end token after logging in successfully, the validity period of the token is set to two hours. When the front-end is saved, the future requests will carry the token, but I did not set all urls of the back-end to be verified. You can add the authentication yourself. Only when the front-end and back-end token authentication is set in /userhome. the token authentication will read MySQL to check whether the user will be allowed to log in, so as to realize the management of user login to the server side. I did not create a super user admin, to add an order type, access /addtype, you can add and delete type,



### Order management module

There are three roles in order management, publisher, order taker and other users, and the three users correspond to different order operation permissions, including publishing orders (including text and files), modifying, deleting, receiving orders, submitting (text and files) as required by the publisher, viewing, downloading, and payment functions. When the payment is clicked, a websocket connection will be established, and the payment result will be returned to the back-end, which will realize the payment result feedback with the established websocket.





### Live chat module

To rely on websocket for real-time connection, redis for state management, text and file sending can be realized, it should be noted that when django starts, I set to empty redis, if not, the connection will be disconnected, but Redis is still online, this error often occurs in development mode. If the user is not online, the message will be stored in MySQL. When the user goes online, the chat data between mysql and local indexDB will be automatically obtained. When the user receives a new message, a new message prompt will appear, which will disappear after reading. Right-click to delete a contact,

# Have a nice day


# 这是一个基于vue3 和python-django的订单管理系统，同时使用了 mysql、indexDB、redis，它可以实现用户管理，订单管理以及实时聊天，可用于用户发布问题悬赏（包含文本和文件），其他用户接单并按照要求解决问题提交相关文本和文件，发布者支付悬赏金额后可查看对方提交的解决方案，发布者确认问题解决后悬赏金额转入对方账户，
此系统部分功能并不完善，前端页面效果还需要美化，代码执行效率较差，错误处理还需要完善，目前我已经不想在写了，因为它太普通了，但愿它对你有用，
在此之前，请自行下载安装redis，以及支持indexDB的浏览器版本，
前端项目启动 cd/orders_vue，

npm install

npm run serve


后端项目启动 cd/orders_djg,

setting.py 
line138 Email configuration
启动Redis

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrete 

python manage.py runserver,

### 用户管理模块
有登录、注册、忘记密码、修改个人信息、邮箱验证，人机验证，Python pillow实现用户人机验证图片信息生成，前端实现点击验证，你可自己修改成滑动、图形等，用户登录成功后即会收到后端token，token的有效期我设置的是两小时，前端保存，以后的请求都会携带token，但我并没设置后端所有URL都验证，你可以自己添加验证，只有在/userhome中设置了前后端token验证，token验证时会读取MySQL查看用户是否会被允许登录，实现用户登录服务端管理，我没有建立超级用户admin，要添加order type，访问 /addtype，可实现type的增加和删除，

### 订单管理模块
订单管理有三种角色，发布者、接单者和其他用户，三种用户对应不同的订单操作权限，有发布订单（包含文本和文件）、修改，删除、接单、按照发布者要求提交（文本和文件）、查看、下载，支付功能我并未完全写出，只写出了逻辑，当点击支付时就会建立websocket连接，支付结果返回后端，后端以建立的websocket实现支付结果反馈，


### 实时聊天模块
以依靠websocket来实现实时连接，redis实现状态管理，可实现文本和文件的发送，需要注意的是当django启动时，我设置了清空redis，如果不这样将会出现连接已断开，Redis却还是在线状态，在开发模式时这个错误会经常出现，生产部署时可视情况删除，如果用户不在线，消息将会存储到MySQL中，用户上线时自动获取mysql和本地indexDB聊天数据，用户收到新消息时会出现新消息提示，读取后将会消失，用户发送和收到的消息将会存储到本地indexdb，右键可删除联系人，

Have a nice day，

