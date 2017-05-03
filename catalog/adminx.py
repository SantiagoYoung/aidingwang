# -*- coding: utf-8 -*-
from models import *
import xadmin
from django import forms
from ckeditor.widgets import CKEditorWidget
from xadmin.plugins.actions import BaseActionView

class goods_detailAdmin(object):
    list_display = ('id','show_index', 'goods_name','belong_to_big','belong_to_small','status','type','current_price','inventory','seller','store','date')
    class MyAction1(BaseActionView):
        action_name = "my_action1"
        description = u'首页点击图片按商品详情展示'
        model_perm = 'change'  #: 该 Action 所需权限

        # 而后实现 do_action 方法
        def do_action(self, queryset):
            # queryset 是包含了已经选择的数据的 queryset
            for obj in queryset:
                obj.type = 0
                obj.save()

    class MyAction2(BaseActionView):
        action_name = "my_action2"
        description = u'首页点击图片按大类列表展示'
        model_perm = 'change'  #: 该 Action 所需权限

        # 而后实现 do_action 方法
        def do_action(self, queryset):
            # queryset 是包含了已经选择的数据的 queryset
            for obj in queryset:
                obj.type = 1
                obj.save()
    class MyAction3(BaseActionView):
        action_name = "my_action3"
        description = u'商品首页展示'
        model_perm = 'change'
        def do_action(self, queryset):
            for ob in queryset:
                ob.show_index = 1
                ob.save()

    class MyAction4(BaseActionView):
        action_name = "my_action4"
        description = u'商品不在首页展示'
        model_perm = 'change'
        def do_action(self, queryset):
            for ob in queryset:
                ob.show_index = 0
                ob.save()

    class MyAction5(BaseActionView):
        action_name = "my_action5"
        description = u'商品待审核'
        model_perm = 'change'

        def do_action(self, queryset):
            for ob in queryset:
                ob.status = 0
                ob.save()

    class MyAction6(BaseActionView):
        action_name = "my_action6"
        description = u'审核中'
        model_perm = 'change'

        def do_action(self, queryset):
            for ob in queryset:
                ob.status = 1
                ob.save()

    class MyAction7(BaseActionView):
        action_name = "my_action7"
        description = u'审核通过'
        model_perm = 'change'

        def do_action(self, queryset):
            for ob in queryset:
                ob.status = 2
                ob.save()


    actions = [MyAction1,MyAction2,MyAction3,MyAction4,MyAction5,MyAction6,MyAction7,]



class send_exampleAdmin(object):
    list_display = ('id','title','body', 'date')
    content = forms.CharField(widget=CKEditorWidget)


class big_goods_typeAdmin(object):
    list_display = ('id','name','create_time','big_picture1','big_picture2','update' )

class small_goods_typeAdmin(object):
    list_display = ('id','name','belong_to_big','create_time', 'update')

class goods_collectionsAdmin(object):
    list_display=('id','goods','user','date','num')

class LunbotuAdmin(object):
    list_display = ('id','date','picture')

class GoodsPictureAdmin(object):
    list_display = ('id','date','goods','picture','picture_id')

class IndexPictureAdmin(object):
    list_diaplay = ('id','index_picture','date')
class GoodsDetailPictureAdmin(object):
    list_display=('id','good','date')


xadmin.site.register(Lunbotu,LunbotuAdmin)
#xadmin.site.register(IndexPicture,IndexPictureAdmin)
xadmin.site.register(big_goods_type,big_goods_typeAdmin)
xadmin.site.register(small_goods_type,small_goods_typeAdmin)
xadmin.site.register(goods_detal,goods_detailAdmin)
xadmin.site.register(GoodsPicture,GoodsPictureAdmin)
xadmin.site.register(GoodsDetailPicture,GoodsDetailPictureAdmin)
xadmin.site.register(send_example,send_exampleAdmin)
xadmin.site.register(goods_collections,goods_collectionsAdmin)

