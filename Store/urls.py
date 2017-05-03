# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url
import views

urlpatterns = [
                       url(r'store_apply/$', views.store_apply, name='store_apply'),           # 申请页面
                       url(r'store_detail/(?P<store_id>[0-9]+/$)', views.store_detail, name='store_detail'),      # 商店详情
                       url(r'store_edit/$', views.store_edit, name='store_edit'),           # 商店资料编辑
                       url(r'show_examination',views.show_examination,name='show_examination'),#店铺待审核列表
                       url(r'store_collection/(?P<goods_detail_id>[0-9]+)', views.store_collection, name='store_collection'),  # 店铺收藏
                       url(r'^design_flow',views.design_flow,name='design_flow'),  # 定制流程
                       url(r'^user_feedback', views.user_feedback, name='user_feedback'), # 意见反馈
                       url(r'^about_us', views.about_us, name='about_us'),  # 关于我们
                       url(r'^contact_us',views.contact_us,name='contact_us'),  # 联系我们
                       url(r'^business_extension',views.business_extension,name='business_extension'), # 商家推广
                       url(r'enterprise_information',views.enterprise_information,name='enterprise_information'), # 企业资料
                       url(r'defined_law',views.defined_law,name='defined_law'),#法律声明
                       url(r'service_list',views.service_list,name='service_list'),#服务协议
                       url(r'my_store', views.my_store, name='my_store'), #我的店铺
                       url(r'register_information',views.register_information,name='register_information'),  #注册信息

                       ]
