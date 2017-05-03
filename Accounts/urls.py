# -*- coding: utf-8 -*-
from django.conf.urls import url, include, patterns
import views
urlpatterns = [
                       url(r'^login/$',views.login,name='login'),#登录
                       url(r'^logout/$',views.logout,name='logout'),#退出登录
                       url(r'^register/$',views.register),#注册
                       url(r'^forget_getcap/$',views.forget_getcap),#忘记密码获取验证码
                       url(r'^forget_password/$',views.forget_password),#忘记密码
                       url(r'^change_password/$',views.change_password),#修改密码
                       url(r'^send_message/$',views.send_message),#系统消息
                       url(r'^accounts_detail/(?P<user_id>[0-9]+)$',views.accounts_detail),#返回用户详情资料
                       url(r'^abouts_us',views.abouts_us),#关于我们界面
                       url(r'message_board',views.message_board,name='message_board'),#留言板
                       url(r'system_information', views.system_information, name = 'system_information'), #系统消息
                       url(r'delete_sysmessage',views.delete_sysmessage,name='delete_sysmessage'),     #删除系统消息
                       url(r'get_meassage', views.get_meassage, name='get_meassage'),  # 留言板
                       url(r'message_board', views.message_board, name='message_board'),  # 留言板
                       url(r'get_messsage_type', views.get_messsage_type, name='get_messsage_type'),  # 留言板
                       url(r'get_default_message', views.get_default_message, name='get_default_message'),  # 留言板
                       url(r'delete_collection_store', views.delete_collection_store, name='delete_collection_store'), #删除收藏店铺
                       url(r'delete_color', views.delete_color, name='delete_color'),#删除颜色
                       url(r'complaint',views.complaint,name='complaint'),#投诉1
                       url(r'tousu',views.tousu,name='complaint'),#投诉2
                       # url('test',views.test)




                       ]


