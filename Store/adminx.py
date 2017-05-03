# -* - coding: utf-8 -*-
from models import Store,customer_suggestions,store_collections

import xadmin
from xadmin.plugins.actions import BaseActionView
class customer_suggestionsAdmin(object):
    list_display = ('id','user','date','body')

class StoreAdmin(object):
    """
            (1, u'审核中'),
        (2, u'通过'),
        (3, u'未通过'),
    """
    list_display = ('id','name','seller','business','kinds','industry','status','character','phone','QQ','headpicture','companyname','connectioner','connection_number','company_adress','company_QQ','date')

    class MyAction1(BaseActionView):
        action_name = "my_action1"
        description = u'审核中'
        model_perm = 'change'

        def do_action(self, queryset):
            for ob in queryset:
                ob.status = 1
                ob.save()

    class MyAction2(BaseActionView):
        action_name = "my_action2"
        description = u'审核通过'
        model_perm = 'change'

        def do_action(self, queryset):
            for ob in queryset:
                ob.status = 2
                ob.save()

    class MyAction3(BaseActionView):
        action_name = "my_action3"
        description = u'审核未通过'
        model_perm = 'change'

        def do_action(self, queryset):
            for ob in queryset:
                ob.status = 3
                ob.save()
    actions = [MyAction1,MyAction2,MyAction3,]

class store_collectionsAdmin(object):
    list_display = ('id', 'store', 'user', 'date', 'num')


xadmin.site.register(Store,StoreAdmin)
xadmin.site.register(customer_suggestions,customer_suggestionsAdmin)
xadmin.site.register(store_collections,store_collectionsAdmin)