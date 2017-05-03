# -*-coding:utf-8 -*-
from models import Store,customer_suggestions,store_collections
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.http.response import HttpResponse, JsonResponse
from helper import check_phone_num
from django.template import RequestContext
from django.shortcuts import render_to_response, render,HttpResponseRedirect
from django.shortcuts import render
from forms import StoreForm,Customer_suggestionsForm
import os
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from Accounts.models import User,MemberInfo
from catalog.models import big_goods_type,goods_detal
from helps.utils import my_admin_required
# Create your views here.
import json
from json import dumps
from django.core.paginator import PageNotAnInteger, InvalidPage, Paginator, EmptyPage

# 开店申请
@login_required
@csrf_exempt
def store_apply(request):
    """
    店铺入驻
    :param request:
    :return:
    'name','seller','business','kinds','link','industry','character','phone','QQ',,'introduction,,
    'headpicture','companyname','connectioner','connection_number','company_adress','company_QQ','business_license'
    """
    user = request.user
    print user
    if request.method =='POST':
        form = StoreForm(request.POST or None, request.FILES or None)
        print "uiosdhfui"
        print form.errors
        if form.is_valid():
            name=form.cleaned_data['name']
            business=form.cleaned_data['business']
            kinds=form.cleaned_data['kinds']
            link=form.cleaned_data['link']
            industry=form.cleaned_data['industry']
            character=form.cleaned_data['character']
            phone=form.cleaned_data['phone']
            QQ=form.cleaned_data['QQ']
            introduction=form.cleaned_data['introduction']
            headpicture=form.cleaned_data['headpicture']
            companyname = form.cleaned_data['companyname']
            connectioner=form.cleaned_data['connectioner']
            connection_number=form.cleaned_data['connection_number']
            company_adress=form.cleaned_data['company_adress']
            company_QQ = form.cleaned_data['company_QQ']
            business_license = form.cleaned_data['business_license']
            company_introduce=form.cleaned_data['company_introduce']

            print headpicture
            print business_license
            print kinds
            # kind = big_goods_type.objects.get(id=kinds)
            # print kind
            # #头像保存
            path = default_storage.save(str(headpicture), ContentFile(headpicture.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            headpicture = str(headpicture)
            #营业执照保存
            path = default_storage.save(str(business_license), ContentFile(business_license.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            business_license = str(business_license)
            s=Store.objects.create(name=name, phone=phone, QQ=QQ,seller=user,
                                 business=business, industry=industry,kinds=kinds,
                                 character=character, introduction=introduction, headpicture=headpicture,
                                 companyname=companyname,link=link,
                                 connectioner=connectioner, connection_number=connection_number,
                                 company_adress=company_adress, company_QQ=company_QQ,
                                 business_license=business_license, company_introduce=company_introduce)
            return render(request,'person_rzcg.html')
        else:
            msg=u'参数填写错误'
            return render(request,'person_dpsq.html',{'msg':msg})
    else:
        return render(request, 'person_dpsq.html', {'forms': StoreForm(),'user':user})
def store_detail(request,store_id):
    """
    店铺详情
    :param request:sssssssssssssss
    :return:
    """
    # if request.method == 'GET':
    #     id = request.GET.get('id')
    #     order = Store.objects.filter(id=id)
    #     return render_to_response('store_detail.html', {'order': order},
    #                               context_instance=RequestContext(request))
    stores = Store.objects.filter(id=store_id)
    render(request,'person_dpxq.html',{'stores':stores})

# 商店资料编辑
@login_required
@csrf_exempt
def store_edit(request):
    """
    商店资料编辑
    :param request:
    :param store_id:
    :return:
    ['name','seller','business','kinds','link','industry','character','phone','QQ','is_create','is_design','is_custom','is_work_design','company','introduction','post','connector']
    """
    try:

        user = request.user
        store = Store.objects.filter(status=2).get(seller=user)
        Aform = StoreForm(instance=store)
    except:
        return HttpResponseRedirect('/Store/store_apply')
    if request.method == 'POST':
        name = request.POST.get('name')
        business = request.POST.get('business')
        kinds = request.POST.get('kinds')
        link = request.POST.get('link')
        industry = request.POST.get('industry')
        character = request.POST.get('character')
        phone = request.POST.get('phone')
        QQ = request.POST.get('QQ')
        introduction = request.POST.get('introduction')
        headpicture = request.FILES.get('headpicture','')
        companyname = request.POST.get('companyname')
        connectioner = request.POST.get('connectioner')
        connection_number = request.POST.get('connection_number')
        company_adress = request.POST.get('company_adress')
        company_QQ = request.POST.get('company_QQ')
        business_license = request.FILES.get('business_license','')
        company_introduce = request.POST.get('company_introduce')

        kind = big_goods_type.objects.get(id=kinds)

        # 头像保存保存# 营业执照保存
        if not headpicture :
            headpicture = store.headpicture
        else:
            path = default_storage.save(str(headpicture), ContentFile(headpicture.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            headpicture = str(headpicture)
        if not business_license:
            business_license = store.business_license
        else:
            path = default_storage.save(str(business_license), ContentFile(business_license.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            business_license = str(business_license)
        s = Store(name=name, phone=phone, QQ=QQ, link=link, kinds=kind,seller=user,
                                 business=business, industry=industry,
                                 character=character, introduction=introduction, headpicture=headpicture,
                                 companyname=companyname,
                                 connectioner=connectioner, connection_number=connection_number,
                                 company_adress=company_adress, company_QQ=company_QQ,
                                 business_license=business_license, company_introduce=company_introduce)
        s.id = store.id
        s.save()
        return HttpResponse('修改成功啦')
    else:
        return render(request,'person_dpbj.html',{'form':Aform})  # else:


@csrf_exempt
@login_required()
def store_collection(request,goods_detail_id):
    '''
    店铺收藏处理
    :param request:
    :return:
    '''
    user = request.user
    goods = goods_detal.objects.get(id=goods_detail_id)
    users = goods.seller
    stores = Store.objects.get(seller=users)
    if request.method == 'POST':
        try:
            status = int(request.POST.get('status'))
        except:
            pass
        try:
            a = store_collections.objects.filter(store=stores)
        except:
            pass
        if not a:
            if status == 1 :
                vv = store_collections.objects.create(store=stores)
                vv.user.add(user)
                vv.save()
                return render(request,'person_spxqy.html',{'msg':u'收藏成功'})
        else:
            if status == 1 :
                for i in a:
                    collectes = store_collections.objects.get(store=stores)
                    collectes.user.add(user)
                    collectes.save()
                    data = {'msg':u'收藏成功','status':200}
                    return HttpResponse(dumps({'data':data}))
            if status == 0:
                collectes = store_collections.objects.get(store=stores)
                collectes.user.remove(user)
                collectes.save()
                data = {'msg': u'取消收藏成功', 'status': 400}
                return HttpResponse(dumps({'data': data}))









@login_required
def show_examination(request):
    """
    @author vincent
    列出提出申请 待审核的商店
    """
    user = request.user
    try:
        store_list = Store.objects.filter(status = 1).get(seller=user)
    except:
        return render(request,'person_dsh.html')
    return render_to_response('person_dsh.html',{'store_list':store_list},
                              context_instance=RequestContext(request))

def design_flow(request):
    """
    定制流程

    :param request:
    :return:
    """
    return render_to_response('person_dzlc.html',context_instance=RequestContext(request))


def user_feedback(request):
    """
   意见反馈

    :param request:
    :return:
    """
    if request.method=='POST':
        form = Customer_suggestionsForm(request.POST)
        if not form.is_valid():
            return render(request,'person_yjfk.html',{'forms':Customer_suggestionsForm})
        types = form.cleaned_data['types']
        body = form.cleaned_data['body']
        phone = form.cleaned_data['phone']
        advices = customer_suggestions(types=types,body=body,phone=phone)
        advices.save()
    else:
        return render(request, 'person_yjfk.html', {'forms': Customer_suggestionsForm})


def about_us(request):
    """
    关于我们

    :param request:
    :return:
    """
    return render_to_response('person_gyadw.html',context_instance=RequestContext(request))


def contact_us(request):
    """
     联系我们
    :param request:
    :return:
    """
    return render_to_response('person_lxwm.html',context_instance=RequestContext(request))


@csrf_exempt
def business_extension(request):
    """
     商家推广
    :param request:
    :return:
    """
    user = request.user
    all_lists = Store.objects.all()
    try:
        lists = Store.objects.get(seller=user)
    except:
        return render(request,'person_qyym.html',{'all_lists':all_lists})
    big = lists.kinds
    print lists.headpicture
    picture = goods_detal.objects.filter(seller=user).all()[0:2]
    return render(request,'person_qyym.html',{'lists':lists,'all_lists':all_lists,'picture':picture, 'big':big})


def enterprise_information(request):
    """
     企业资料
    :param request:
    :return:
    """
    return render_to_response('person_qyzl.html',context_instance=RequestContext(request))


def defined_law(request):
    """
    法律声明
    :param request:
    :return:
    """
    return render(request,'person_flsm.html')

def service_list(request):
    """
    服务协议
    :param request:
    :return:
    """
    return render(request,'person_fwxy.html')


    # 我的店铺

def my_store(request):
    """
    我的店铺
    :param request:
    :return:
    """
    user = request.user
    try:
        store = Store.objects.filter(seller=user)
    except:
        return render(request,'person_wddp.html')
    return render(request, 'person_wddp.html', {'store': store})


@login_required()
def register_information(request):
    """
    注册信息
    :param request:
    :return:
    """
    user = request.user
    try:
        info = MemberInfo.objects.get(user=user)
    except:
        return render(request,'person_zcxx.html')
    return render(request, 'person_zcxx.html', {'user':user,'info':info})
