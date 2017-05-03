# -*- coding: utf-8 -*-
from django.conf.urls import url
import views

urlpatterns=[
    url(r'^show_type',views.show_type,name='show_type'),#上传分类
    url(r'^goods_detail/(?P<goods_detail_id>[0-9]+)',views.goods_detail,name='goods_detail'),#商品详情
    url(r'goods_edit/(?P<goods_detail_id>[0-9]+)',views.goods_edit,name='goods_edit'),#商品修改
    url(r'^send_goods',views.send_goods,name='send_goods'),#上传商品
    url(r'^upload_demo',views.upload_demo,name='upload_demo'),#上传商品示例
    url(r'^comments/(?P<goods_detail_id>[0-9]+)',views.comments,name='comments'),#评论
    url(r'^collections/(?P<goods_detail_id>[0-9]+)',views.collections,name='collections'),#商品收藏
    url(r'^search',views.search,name='search'),#搜索
    url(r'^user_collections_list',views.user_collections_list,name='user_collections_list'),#我的收藏页面
    url(r'show_goods/(?P<goods_detail_id>[0-9]+)',views.show_goods,name='big_goods_type'),#按大类展示商品
    url(r'ShowGoodsByBigType/(?P<big_goods_type_id>[0-9]+)',views.ShowGoodsByBigType,name='ShowGoodsByBigType'),#按大类展示商品
    url(r'ShowGoodsBySmallType/(?P<small_goods_type_id>[0-9]+)',views.ShowGoodsBySmallType,name='ShowGoodsBySmallType'),#按小类展示商品
    url(r'show_name',views.show_name,name='show_name'),#展示商品大小种类名字
    url(r'sell_room/(?P<type_id>[0-9]+)',views.sell_room,name='sell_room'),#销售中心
    url(r'delete_collections_goods',views.delete_collections_goods,name="delete_collections_goods"),#删除我的收藏
    url(r'del_seller_core',views.del_seller_core,name='del_seller_core'),#删除销售中心的内容
    url(r'store_collection_list', views.store_collection_list, name='store_collection_list'),  # 店铺收藏页面
    url(r'delete_uploaded_picture', views.delete_uploaded_picture, name='delete_uploaded_picture'), #删除上传图片
]