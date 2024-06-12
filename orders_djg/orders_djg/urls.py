
from django.contrib import admin
from django.urls import path
from app import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/test',views.test),
    path('api/signup',views.signup),
    path('api/emailauth',views.emailauth),
    path('api/usernamedete',views.usernamedete),
    path('api/robotverify',views.robotverify),
    path('api/login',views.login),
    path('api/verifytoken',views.verify_token),
    path('api/userdata',views.userdata),
    path('api/userupdate',views.userupdate),
    path('api/addorder',views.addorder),
    path('api/typehandle',views.typehandle),
    path('api/getorders',views.getorders),
    path('api/getorderdetail',views.getorderdetail),
    path('api/filedown',views.filedown),
    path('api/updataorder',views.updataorder),
    path('api/filterdata',views.filterdata),
    path('api/message',views.message),
    path('api/messagefile',views.messagefile),
    path('api/payment',views.payment),
    path('api/receiveorder',views.receiveorder),
    path('api/mytask',views.mytask),
    path('api/orderfinish',views.orderfinish),
    path('api/gettext',views.gettext),
    path('api/surefinish',views.surefinish),
    path('api/repwd',views.repwd),

]
