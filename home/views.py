# -*- coding: utf-8 -*-
from django.shortcuts import render
from catalog.models import *
from django.contrib.auth.decorators import user_passes_test
from helps.utils import user_check
# Create your views here.


@user_passes_test(user_check,login_url="/Accounts/logout")
def index(request):
    """
    主页
        INDEX= (
        (0,u'不在首頁展示'),
        (1,u'在首頁展示')
    )
    :param request:
    :return:
    """
    user = request.user
    data = []
    try:
        lunbotu = Lunbotu.objects.all().order_by('-date')[0:5]
    except:
        pass
    index_pictures = goods_detal.objects.filter(show_index=1).all().order_by('-id')
    index_picture = list(index_pictures)[0:4]
    try:
        big_type = list(big_goods_type.objects.all())
    except:
        pass
    for i in big_type:
        big_type_name=i.name
        big_id = i.id
        big_picture1 = str(i.big_picture1)
        big_picture2 = str(i.big_picture2)
        goods = goods_detal.objects.filter(belong_to_big=i).filter(show_index=1).filter(status=2)
        ls=[]
        for m in goods:
            p = str(m.picture)
            n = str(m.goods_name)
            cp = int(m.current_price)
            id = int(m.id)
            u={'p':p,'n':n,'cp':cp,'id':id}
            ls.append(u)
        data.append({'big_type_name':big_type_name,'big_id':big_id,'big_picture1':big_picture1,'big_picture2':big_picture2,'goods':ls})
    return render(request, 'person_home.html', {'lunbotu_list': lunbotu,'index_picture':index_picture,'data':data , 'user':user})
