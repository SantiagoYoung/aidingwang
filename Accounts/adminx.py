# -*- coding: utf-8 -*-
from Accounts.models import *
import xadmin
from xadmin import views
from django.contrib.auth.models import Group, Permission
from xadmin.plugins.actions import BaseActionView


class MainDashBoard(object):
    widgets = [
        [
            {'type': 'html', 'title': u'Paper 后台管理', 'content': '<h3>欢迎来到<strong>爱定网</strong>后台管理系统</h3>'
                                                                '<p>开发团队：黑虎工作室</p><p>联系方式：183-4925-3806</p>'
                                                                '<p>联系人：石子星</p>'},
        ],
    ]


xadmin.site.register(views.website.IndexView, MainDashBoard)


class UserAdmin(object):
    list_display = (
            "id","username", "is_active", "date_joined"
        )

    ordering = ("-date_joined",)


# class MemberInfoAdmin(object):
#     list_display = (
#         "user", "linkman", "phone_number", "email", "credits"
#     )

xadmin.site.unregister(User)
xadmin.site.register(User, UserAdmin)
xadmin.site.register(MemberInfo)
# xadmin.site.register(MemberInfoAdmin)


class BaseSetting(object):
    enable_themes = False
    enable_bootswatch = False


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSetting(object):
    apps_label_title = {
        'auth': u'权限',
        'accounts': u'用户管理',
        'store': u'店铺',
        'catalog':u'商品详情'

    }
    site_title = u'爱定网'
    site_footer = u'成都智橙科技有限公司'
    menu_style = 'default'
class message_boardAdmin(object):
    list_display = ('id','type','content','create_time','stick','status')
    class MyAction1(BaseActionView):
        action_name = "my_action1"
        description = u'展示留言'
        model_perm = 'change'  #: 该 Action 所需权限

        # 而后实现 do_action 方法
        def do_action(self, queryset):
            # queryset 是包含了已经选择的数据的 queryset
            for obj in queryset:
                obj.status = 0
                obj.save()

    class MyAction2(BaseActionView):
        action_name = "my_action2"
        description = u'暂不展示'
        model_perm = 'change'  #: 该 Action 所需权限

        # 而后实现 do_action 方法
        def do_action(self, queryset):
            # queryset 是包含了已经选择的数据的 queryset
            for obj in queryset:
                obj.status = 1
                obj.save()
    # actions=[MyAction1,MyAction2,]

class send_messageAdmin(object):
    list_display = ('id','receiver','message_subject','message','send_time')


class Messsage_TypeAdmin(object):
    list_display = ('id','type')


class ComplantAdmin(object):
    list_display = ('id','name','body','date')

# class Message_CommentAdmin(object):
#     list_display = ('id','comment','comment_time')

xadmin.site.register(views.CommAdminView, GlobalSetting)

xadmin.site.unregister(Group)
xadmin.site.unregister(Permission)
xadmin.site.register(send_message,send_messageAdmin)
xadmin.site.register(Message_Board,message_boardAdmin)
# xadmin.site.register(Messsage_Type,Messsage_TypeAdmin)
xadmin.site.register(Complant,ComplantAdmin)
# xadmin.site.register(Message_Comment,Message_CommentAdmin)