# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response,HttpResponseRedirect
from django.template import RequestContext
from models import *
from django.shortcuts import HttpResponse
import os
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from Store.models import Store
from django.db.models import Q
from forms import SendGoods
from json import dumps
from Accounts.models import User
from Store.models import Store
from helps.paginator import Getpag
from django.contrib.auth.decorators import user_passes_test
from helps.utils import user_check
from Store.models import Store,store_collections
from django.core.paginator import PageNotAnInteger, InvalidPage, Paginator, EmptyPage

def global_variable(request):
    """
    basic页面传值
    :param request:
    :return:
    """
    big_types = big_goods_type.objects.all()
    big_small = {}
    for big_type in big_types:
        small_types = small_goods_type.objects.filter(belong_to_big=big_type)
        big_small[big_type] = small_types

    user = request.user
    store = ''
    try:
        store = Store.objects.get(seller=user)
    except:
        pass
    if store:
        return {'big_small':big_small,'store':store}
    else:
        return {'big_small': big_small}


def show_type(request):
    """
    上传商品分类
    :param request:
    :param slug_big:
    :return:
    """
    all_big_type = big_goods_type.objects.all().order_by('id')
    data = []
    for p in all_big_type:
        b_name = p.name
        all_small_type = small_goods_type.objects.filter(belong_to_big=p)
        s_name = []
        s_id =[]
        for k in all_small_type:
            s_name.append(k.name)
            s_id.append(k.id)
        data.append({'big':b_name,'small':s_name,'id':s_id})
    return HttpResponse(dumps({'data':data}))


def show_name(request):
    """
    上传商品分类名字,后台操作
    :param request:
    :param slug_big:
    :return:
    """
    data=[]
    all_big_type = big_goods_type.objects.all().order_by('id')
    good_picture = []
    for p in all_big_type:
        b_name = p.name
        b_id = p.id
        good_picture.append(p.big_picture1)
        all_small_type = small_goods_type.objects.filter(belong_to_big=p)
        s_data = []
        for k in all_small_type:
            u = {'s_name':k.name,'s_id':k.id, 'k':k }
            s_data.append(u)
        data.append({'b_name':b_name,'b_id':b_id,'s_data':s_data})
    return render(request,'person_jpdz.html',{'datas':data})



def goods_detail(request,goods_detail_id):
    """
    商品详情
    :param request:
    :return:
    """
    user = request.user
    show_picture = GoodsPicture.objects.filter(goods_id=goods_detail_id)
    detail_picture=GoodsDetailPicture.objects.filter(good_id=goods_detail_id)
    picture = show_picture[0:3]
    goods_details = goods_detal.objects.get(id=goods_detail_id)
    goods_details_color = goods_details.color.split(',')
    store_user = goods_details.seller
    store = Store.objects.get(seller=store_user)
    # num = goods_collections.objects.get()
    if user.is_anonymous():
        data = {'goods_details':goods_details,'show_picture':show_picture,'goods':u'收藏商品','store':u'收藏店铺',"picture":picture,'detail_picture':detail_picture}
        return render(request,'person_spxqy.html', {'data': data, 'store': store,"pictures":picture,})
    else:
        try:
            goods_info = goods_collections.objects.get(goods=goods_details)
        except:
            goods_info = 0
        try:
            store_info = store_collections.objects.get(store=store)
        except:store_info = 0

        g =0
        s =0
        if goods_info !=0:
            if user in goods_info.user.all():
                g=u'取消收藏'
            else:
                g=u'收藏商品'
        else:
            g = u'收藏商品'
        if store_info != 0:
            if user in store_info.user.all():
                s = u'取消收藏'
            else:
                s = u'收藏店铺'
        else:
            s = u'收藏店铺'

        data = {'goods_details': goods_details, 'show_picture': show_picture, 'goods':g,'store':s,'detail_picture':detail_picture }
        return render(request,'person_spxqy.html',{'data':data,'colors': goods_details_color, 'store':store,"pictures":picture})



def show_goods(request,goods_detail_id):
    """
    点击主页图片展示内容
      CHOICE = (
        (0,u'按商品详情展示'),
        (1,u'按大类列表展示'),
    )
    :param request:
    :return:
    """
    user = request.user
    goods = goods_detal.objects.get(id=goods_detail_id)
    type = goods.type
    if type == 0:
        return goods_detail(request,goods_detail_id)
    if type == 1:
        belong_to_small = goods.belong_to_small
        big_name = goods.belong_to_big.name
        small_name = small_goods_type.objects.filter(belong_to_big=goods.belong_to_big)
        AllGoods = goods_detal.objects.filter(belong_to_small=belong_to_small).all()
        s_name = AllGoods[0].belong_to_small.name
        data = []
        for i in AllGoods:
            p = str(i.picture)
            n = str(i.goods_name)
            cp = int(i.current_price)
            u = {'picture':p,'name':n,'price':cp,'id':i.id}
            data.append(u)
        return render(request,'person_sy_spxl.html',{'big_name':big_name,'small_name':small_name,'s_name':s_name,'data':data})


def ShowGoodsByBigType(request,big_goods_type_id):
    """
    按大类展示商品
    :param request:
    :param big_goods_type_id:
    :return:
    """
    data=[]
    big_type = big_goods_type.objects.get(id=big_goods_type_id)
    small_type = small_goods_type.objects.filter(belong_to_big=big_type).order_by('update')
    s= list(small_type)[0]
    print s.name

    print type(s)
    show_lists = goods_detal.objects.filter(belong_to_small=s).filter(status=2)

    for i in small_type:
        s_name = i.name
        goods = goods_detal.objects.filter(belong_to_small=i).filter(status=2)
        u={'s_name':s_name,'s_id':i.id,'goods':goods}
        data.append(u)
    return render(request, 'person_spdl.html', {'data':data,'big_type':big_type,'show_lists':show_lists,'small':s})


def ShowGoodsBySmallType(request,small_goods_type_id):
    """
    按小类展示商品
    :param request:
    :param small_goods_type_id:
    :return:
    """
    small_type = small_goods_type.objects.get(id=small_goods_type_id)
    s_name = small_type.name
    big_type = small_type.belong_to_big
    big_name = big_type.name
    all_small = small_goods_type.objects.filter(belong_to_big=big_type)
    goods = goods_detal.objects.filter(belong_to_small=small_type).filter(status=2)
    paginator = Paginator(goods, 8)
    page = request.GET.get('page')
    try:
        good = paginator.page(page)
    except(PageNotAnInteger, InvalidPage ):
        good = paginator.page(1)
    except EmptyPage:
        good = paginator.page(paginator.num_pages)

    data = {'s_name': s_name, 's_id': small_type.id,}


    return render(request, 'person_spxl.html', {'data': data,'big_name':big_name,'all_small':all_small,
                                                'paginator':paginator,'good':good})


@user_passes_test(user_check)
@login_required(login_url='/')
def send_goods(request):
    """
    上传商品
    :param request:
    :return:
    """
    forms=SendGoods
    user=request.user
    if request.method == 'POST':
        form = SendGoods(request.POST,request.FILES)
        if not form.is_valid():
            msg = u'请填写完整'
            return render(request, 'person_scspsb.html', {'msg': msg})
        try:
            id = request.POST.get('belong_to_small')
            goods_name = request.POST.get('goods_name',None)
            picture = request.FILES.get('picture',None)
            original_price = str(request.POST.get('original_price',None))
            current_price = str(request.POST.get('current_price',None))
            color = request.POST.get('color',None)
            is_provide_design = request.POST.get('is_provide_design', False)
            is_provide_make = request.POST.get('is_provide_make', False)
            is_customize_size = request.POST.get('is_customize_size', False)
            inventory = request.POST.get('inventory',0)
            is_customize_patten = request.POST.get('is_customize_patten', False)
            is_customize_style = request.POST.get('is_customize_style', False)
            goods_url = request.POST.get('goods_url',None)
            goods_picture_lists = request.FILES.getlist('goods_picture',None)
            goods_detail_picture=request.FILES.getlist('goods_detailpicture',None)
            goods_introduce = request.POST.get('goods_introduce',None)
            server_introduce = request.POST.get('server_introduce',None)
            print goods_picture_lists
        except:
            pass
        s = list(goods_url)
        if s[0:4] == ['h','t','t','p'] or s[0:5] == ['h','t','t','p','s']:
            goods_url = goods_url
        else:
            goods_url = "http://"+goods_url
        store = Store.objects.get(seller=user).name
        if not store:
            return HttpResponseRedirect("/Store/store_apply")
        store_type = Store.objects.get(seller=user).status
        if store_type != 2:
            return HttpResponse("店铺未通过审核")
        belong_to_small = small_goods_type.objects.get(id=id)
        belong_to_big = belong_to_small.belong_to_big
        t = goods_detal.objects.filter(goods_name=goods_name,goods_url=goods_url)
        if t:
            msg = u'请勿重复上传商品'
            return render(request,'person_scspsb.html',{'msg':msg})
        s=goods_detal.objects.create(
            original_price=original_price,current_price=current_price,goods_name=goods_name,picture=picture,color=color,
            is_provide_design=is_provide_design, is_provide_make=is_provide_make,belong_to_big=belong_to_big,store=store,
            is_customize_size=is_customize_size, is_customize_patten=is_customize_patten,belong_to_small=belong_to_small,
            is_customize_style=is_customize_style, goods_url=goods_url, inventory=inventory,goods_introduce=goods_introduce,
            server_introduce=server_introduce,seller=user,
        )

        s.save()
        for picture in goods_picture_lists:
            path = default_storage.save(str(picture), ContentFile(picture.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            picture_path = str(picture)
            GoodsPicture.objects.create(picture_id=0,goods_id=s.id,picture=picture)
        for picture_detail in goods_detail_picture:
            path = default_storage.save(str(picture_detail), ContentFile(picture_detail.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            picture_path = str(picture_detail)
            GoodsDetailPicture.objects.create(good_id=s.id,picture_detail=picture_detail)
        return render(request, 'person_sccg.html')
    else:
        return render(request,'person_scsp.html',{'form':forms})


@login_required()
@csrf_exempt
def goods_edit(request,goods_detail_id):
    """
    商品编辑
    :param request:
    :param goods_detail_id:
    :return:
    """
    print goods_detail_id

    try:
        print "ooooook"
        user = request.user
        print user
        goods= goods_detal.objects.get(id=goods_detail_id)

        print goods

        ASendGood = SendGoods(instance=goods)
        show_picture = GoodsPicture.objects.filter(goods=goods)
        picture_detail=GoodsDetailPicture.objects.filter(good=goods)
    except:
        return HttpResponse("错误")
    if request.method == "POST":
        try:
            id = request.POST.get('belong_to_small')
            goods_name = request.POST.get('goods_name')
            picture = request.FILES.get('picture',0)
            original_price = str(request.POST.get('original_price'))
            current_price = str(request.POST.get('current_price'))
            color = request.POST.get('color')
            is_provide_design = request.POST.get('is_provide_design', False)
            is_provide_make = request.POST.get('is_provide_make', False)
            is_customize_size = request.POST.get('is_customize_size', False)
            inventory = request.POST.get('inventory', 0)
            is_customize_patten = request.POST.get('is_customize_patten', False)
            is_customize_style = request.POST.get('is_customize_style', False)
            goods_url = request.POST.get('goods_url',)
            goods_introduce = request.POST.get('goods_introduce')
            server_introduce = request.POST.get('server_introduce')
            goods_picture_lists = request.FILES.getlist('goods_picture', None)
            print goods_picture_lists
        except:
            pass
        print goods_url
        s = list(goods_url)
        store = Store.objects.get(seller=user).name
        if s[0:4] == ['h', 't', 't', 'p'] or s[0:5] == ['h', 't', 't', 'p', 's']:
            goods_url = goods_url
        else:
            goods_url = "http://" + goods_url
        belong_to_small = small_goods_type.objects.get(id=id)
        belong_to_big = belong_to_small.belong_to_big
        if not picture:
            picture_path = goods.picture
        else:
            path = default_storage.save(str(picture), ContentFile(picture.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            picture_path = str(picture)

        s = goods_detal(
            original_price=original_price, current_price=current_price, goods_name=goods_name, picture=picture_path,
            color=color,seller=goods.seller,store=store,
            is_provide_design=is_provide_design, is_provide_make=is_provide_make, belong_to_big=belong_to_big,
            is_customize_size=is_customize_size, is_customize_patten=is_customize_patten,
            belong_to_small=belong_to_small,
            is_customize_style=is_customize_style, goods_url=goods_url, inventory=inventory,
            goods_introduce=goods_introduce,
            server_introduce=server_introduce,

        )
        s.id = goods.id
        s.save()
        if goods_picture_lists:
            for picture in goods_picture_lists:
                path = default_storage.save(str(picture), ContentFile(picture.read()))
                tmp_file = os.path.join(settings.MEDIA_ROOT, path)
                picture_path = str(picture)
                GoodsPicture.objects.create(picture_id=0, goods_id=s.id, picture=picture)

        return render(request, 'person_bjspcg.html')
    else:
        return render(request, 'person_spbj.html', {'form': ASendGood,'show_picture':show_picture,'goods':goods,'picture_detail':picture_detail})



def delete_goods(request):
    """
    删除商品
    :param request:
    :return:
    """
    if request.methon=="POST":
        id_list = request.POST.getlist("id[]")
        for i in id_list:
            goods = goods_detal.objects.get(id=i)
            goods.type=3
            goods.save()

def upload_demo(request):
    """
    上传商品实例
    :param request:
    :return:
    """

    goods_detail = send_example.objects.all().order_by('id')
    print goods_detail
    if goods_detail:

        a = goods_detail[0]
        title = a.title
        body = a.body
        return render(request,'person_scfl.html',{'goods_detail_title':title,'goods_detail_body':body},context_instance=RequestContext(request))
    return render(request,'person_scfl.html')

@login_required
@csrf_exempt
def comments(request,goods_detail_id):
    """
    评论商品
    :param request:
    :return:
    """
    user=request.user
    if request.method == 'POST':
        try:
            coments = request.POST.get('coments')
        except:
            pass
    goods = goods_detal.objects.filter(id=goods_detail_id)
    goods_coments.objects.create( user=user, goods=goods, coments=coments )
    return render_to_response('',context_instance=RequestContext(request))

@login_required()
@csrf_exempt
def collections(request,goods_detail_id):
    """
    商品收藏处理
    1->收藏
    0->取消收藏
    :param request:
    :return:
    """
    print goods_detail_id
    user = request.user
    goods = goods_detal.objects.get(id=goods_detail_id)
    print goods
    if request.method == 'POST':
        try:
            status = int(request.POST.get('status'))
            print status
        except:
            pass
        try:
            a = goods_collections.objects.filter(goods=goods)
        except:
            pass
        if not a:
            num = 0
            if status == 1 :
                vv = goods_collections.objects.create(goods=goods,num=num)
                vv.user.add(user)
                vv.save()
                return render(request,'person_spxqy.html',{'msg':u'收藏成功'})
        else:
            if status == 1 :
                print status, ">>>>>>>>>>>>>>>>>>>>"
                collectes = goods_collections.objects.get(goods = goods)
                collectes.user.add(user)
                collectes.save()
                data = {'msg':u'收藏成功','status':200}
                return HttpResponse(dumps({'data':data}))
            if status == 0:
                collectes = goods_collections.objects.get(goods=goods)
                collectes.user.remove(user)
                collectes.save()
                data = {'msg': u'取消收藏成功', 'status': 400}
                return HttpResponse(dumps({'data': data}))



@csrf_exempt
def search(request):
    """
    按商店或则是商品搜索
    0->代表按照商品
    1->代表按照商铺
    :param request:
    :return:
    """

    goods_search = request.GET.get('goods_search')
    shop_search = request.GET.get('store_name')
    page = request.GET.get('page')
    print shop_search
    print goods_search

    if not goods_search and not shop_search :
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

    if goods_search:
        goods_list = goods_detal.objects.filter(Q(goods_name__icontains=goods_search)&Q(status='2'))
        if  not goods_list:
            return render(request,'person_searcnull.html')

        paginator = Paginator(goods_list, 8)
        try:
            goods = paginator.page(page)
        except (PageNotAnInteger, InvalidPage):
            goods = paginator.page(1)
        except EmptyPage:
            goods = paginator.page(paginator.num_pages)

        return render(request, 'person_goods_search.html',
                      {'paginator': paginator, 'goods': goods, 'goods_search': goods_search})
    if shop_search:
        shop_lists = Store.objects.filter(Q(name__icontains=shop_search)&Q(status='2'))
        if not shop_lists:
            return render(request,'person_searcnull.html')

        paginator = Paginator(shop_lists, 8)
        try:
            stores = paginator.page(page)
        except (PageNotAnInteger, InvalidPage):
            stores = paginator.page(1)
        except EmptyPage:
            stores = paginator.page(paginator.num_pages)

        return render(request, 'person_store_search.html',
                      {'pagenator':paginator,'stores': stores,'shop_search': shop_search})
    return HttpResponseRedirect('/')


@login_required()
def user_collections_list(request):
    """
    用户收藏商品页
    :param request:
    :return:
    """
    user = request.user
    data = []
    detail = goods_collections.objects.filter(user=user).all().order_by('-date')

    for i in detail:
        a = i.goods.id
        goods = goods_detal.objects.get(id=a)
        data.append(goods)

    paginator = Paginator(detail, 8)
    page = request.GET.get('page')
    try:
        goods = paginator.page(page)
    except (InvalidPage, PageNotAnInteger):
        goods = paginator.page(1)
    except EmptyPage:
        goods = paginator.page(paginator.num_pages)

    return render(request,'person_scdsp.html',{'data':data, 'paginator':paginator, 'goods': goods,'detail':detail})



@login_required()
@csrf_exempt
def store_collection_list(requset):
    """
    用户收藏的店铺
    :param requset:
    :return:
    """
    user = requset.user
    store = store_collections.objects.filter(user=user)
    stores = []
    for i in store:
        id =i.store.id
        s = Store.objects.get(id=id)
        stores.append(s)
    paginator = Paginator(store, 8)
    page = requset.GET.get('page')
    try:
        stores = paginator.page(page)
    except (InvalidPage, PageNotAnInteger):
        stores = paginator.page(1)
    except EmptyPage:
        stores = paginator.page(paginator.num_pages)


    return render(requset, 'person_scddp.html',{'stores': stores, 'paginator':paginator,'store':store})

@login_required()
@csrf_exempt
def sell_room(request,type_id):
    """   商品状态：     (0, u'审核中'),
        (1, u'未通过'),
        (2, u'审核通过'),
        (3,u'已过期')
    type_id
    0->审核中
    1->未通过
    2-> 销售中
    3->已销售（已过期）
    :param request:
    :return:
    """
    user=request.user
    try:
        goods_lists = goods_detal.objects.filter(seller=user)
    except:
        return render(request,'person_xszx.html')
    goods_list = goods_lists.filter(status=type_id).all()
    paginator = Paginator(goods_list, 8)
    page = request.GET.get('page')
    try:
        sell_goods = paginator.page(page)
    except (PageNotAnInteger, InvalidPage):
        sell_goods = paginator.page(1)
    except EmptyPage:
        sell_goods = paginator.page(paginator.num_pages)
    return render(request,'person_xszx.html',{'goods_list':goods_list, 'paginator': paginator, 'sell': sell_goods})


@login_required()
@csrf_exempt
def delete_collections_goods(request):
    """
    删除收藏商品
    :param request:
    :return:
    """
    user=request.user
    if request.method == 'POST':
        try:
            id_lists = request.POST.getlist('id[]')
        except:
            pass
        print id_lists
        for i in id_lists:
            goods=goods_detal.objects.get(id=i)
            collections = goods_collections.objects.get(goods=goods)
            collections.user.remove(user)
            collections.save()
        return HttpResponse(dumps({'data': u'删除成功', 'status': 200}))



@login_required()
@csrf_exempt
def del_seller_core(request):
    """
    删除销售中心的商品
    :param request:
    :return:
    """
    if request.method == "POST":
        try:
            id_list = request.POST.getlist('id[]','')
        except:
            pass
        print id_list
        for i in id_list:
            goods = goods_detal.objects.get(id=i)
            status = goods.status
            print status
            if status==3:
                goods.delete()
            else:
                goods.status=3
                goods.save()
        return HttpResponse(dumps({'data':u'删除成功','status':200}))

@login_required()
@csrf_exempt
def delete_uploaded_picture(request):
    """
    删除编辑图片
    :param request:
    :return:
    """
    if request.method == 'POST':
        try:
            id_list = request.POST.getlist('id[]')
        except:
            pass
        print id_list
        for i in id_list:
            uploaded_picture = GoodsPicture.objects.get(id=i)
            uploaded_picture.delete()
        return HttpResponse(dumps({'data':u'删除成功','status':200}))
