# -*- coding: utf-8 -*-
from django.contrib import auth  # 不与上面共同导入是因为下面要写login函数, 避免重名
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail,send_mass_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from helps.test import check_email,get_code
from helps.utils import json_response,my_admin_required,paginator
from Store.models import Store
from models import *
from models import User
import json
from json import dumps
from django.contrib import auth
from django.contrib.auth import login as lg
# from forms import Message_boardForm
from django.contrib import messages
# from test import LoginForm

from django.http import JsonResponse
from Store.models import store_collections
from catalog.models import goods_detal

from django.core.paginator import PageNotAnInteger, InvalidPage, Paginator, EmptyPage
from django.http import JsonResponse





@csrf_exempt
def login(request):
    """
    登录
    邮箱作为用户的唯一信息，唯一识别
    :param request:
    :return:
    """
    if request.method == 'POST':
        try:
            username = request.POST.get("email")
            password = request.POST.get("password")
            if not check_email(username):
                msg = u'邮箱格式不对'
                return render(request, 'person_login.html', {'msg': msg})
        except Exception:
            msg = u'参数错误，请重试'
            return render(request,"person_login.html",{'msg':msg} )
        try:
            u=User.objects.get(username=username)
        except User.DoesNotExist:
            msg = u'该用户不存在'
            status = '404'
            return render(request, "person_login.html", {'msg': msg})
        try:
            usr=auth.authenticate(username=username, password=password)
            auth.login(request, usr)
        except Exception:
            msg = u'邮箱和密码不匹配，请重试'
            return render(request, "person_login.html", {'msg': msg})
        return HttpResponseRedirect('/')
    else:
        return render(request,"person_login.html")


@login_required()
def logout(request):
    """
    退出
    :param request:
    :return:
    """
    auth.logout(request)
    return HttpResponseRedirect(redirect_to='/')

@csrf_exempt
def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.method == 'POST':
        try:
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            username = request.POST.get('email')
            name = request.POST.get('nickname')
            phone = request.POST.get('phone')
            QQ = request.POST.get('QQ')
        except:
            msg = u'请将注册信息填写完整！！！'
            return render(request,'person_zc.html',{'msg':msg})
        if not check_email(username):
            msg = u'邮箱格式不正确'
            return render(request, 'person_zc.html', {'msg': msg})
        if password ==confirm_password:
            user_list = [user.username for user in User.objects.all()]
            if username in user_list:
                msg=u'用户已存在'
                return render(request, 'person_zc.html', {'msg': msg})
            else:
                user = User.objects.create_user(username=username,password=password)
                MemberInfo.objects.create(user=user,phone_number=phone, qq_number=QQ, linkman=name)
                return render(request, 'person_login.html')
        else:
            msg=u'密码不一样'
            return render(request, 'person_zc.html',{'msg':msg})
    else:
        return render(request,'person_zc.html')


@csrf_exempt
def forget_getcap(request):
    """
    忘记密码，获取验证码
    """
    if request.method == "POST":
        username = request.POST.get("email")
        if not check_email(username):
            msg = u'邮箱格式不对\n'
            return render(request, 'person_wjmm.html', {'msg': msg})
        user_list = [user.username for user in User.objects.all()]
        if username not in user_list:
            print "ok"
            msg = u'用户不存在！'
            return render(request, 'person_wjmm.html', {'msg': msg})
        code = get_code()
        text = "【爱定网】您的验证码是" + str(code)
        s= u'爱定网'
        send_mail(s, text, 'aidingwang@126.com',[username], fail_silently=False)

     # 设置session的过期时为60s
        EXPIRE_TIME = 60
        verify_code = {'verify_code': code}
        request.session[username] = verify_code#把验证码存到session里
        request.session.set_expiry(EXPIRE_TIME)#设置过期时间
        msg=u'验证码已失效'
        return render(request, 'person_wjmm.html', {'msg': msg})
    return json_response(results=[],status='', message='')


@csrf_exempt
def forget_password(request):
    """
    忘记密码
    """
    if request.method == "GET":
        try:
            username = request.GET.get('email')
            password = request.GET.get('password')
            confirm_password = request.GET.get('confirm_password')
            captcha = request.GET.get('captcha')#验证码
        except:
            pass

        if not username or not password or not captcha or not confirm_password:
            msg = u'请填写完整'
            return render(request,'person_wjmm.html',{'msg':msg})
        print "wrong"
        try:
            verify_code = request.session.get(username).get('verify_code')
        except AttributeError:
            msg = u'验证码失效，请重新获取'
            return render(request, 'person_wjmm.html', {'msg': msg})

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            msg = u'用户不存在'
            return render(request, 'person_wjmm.html', {'msg': msg})
        print "ok"

        if captcha != verify_code:
            msg = u'验证码不正确'
            return render(request, 'person_wjmm.html', {'msg': msg})
        if captcha == verify_code and password==confirm_password:
            # 设置session过期
            request.session.set_expiry(0)
            user.set_password(password)
            user.save()
            return render(request,'person_xgcg.html')
    else:
        return render_to_response('person_wjmm.html',context_instance=RequestContext(request))

@csrf_exempt
@login_required()
def change_password(request):
    """
    修改密码（知道原密码）
    :param request:
    :return:
    """
    user = request.user
    if request.method == 'POST':
        origin_password = request.POST.get('origin_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm')
        if user.check_password(origin_password) and new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            messages.info(request, '修改密码成功')
            s = u'修改密码成功'
            return render_to_response('person_login.html')
        else:
            s = u'用户与密码不匹配'
            return render_to_response('person_xgmm.html', {'message': s})
    return render_to_response('person_xgmm.html', context_instance=RequestContext(request))


@login_required
def accounts_detail(request,user_id):
    """
    返回用户详情资料
    :param request:
    :return:
    """
    detail = MemberInfo.objects.get(id=user_id)
    return render_to_response('person_wdzl.html', {'detail': detail})

def abouts_us(request):
    """
    关于我们界面
    :param request:
    :return:
    """
    return render_to_response('about_us.html',context_instance=RequestContext(request))

def get_default_message(request):
    """
    留言板
    :param request:
    :return:
    """
    type = request.GET.get('type_id',None)
    if type == None:
        try:
            type = Messsage_Type.objects.get(id = 1 )
        except Messsage_Type.DoesNotExist:
            content = {'status':0,'msg':'can not find this Type'}
            return HttpResponse( json.dumps(content),content_type='application/json')
    else:
        try:
            type = Messsage_Type.objects.get(type=type)
        except Messsage_Type.DoesNotExist:
            content = {'status':0,'msg':"请选择正确的类型"}
            return HttpResponse(json.dumps(content),content_type='application/json')
    message_set = Message_Board.objects.filter(type=type).filter(status=0).order_by('stick')
    if message_set:
        paginator = Paginator(message_set, 6)
        total_page =  paginator.num_pages
        page = request.GET.get('page',None)
        try:
            message_s = paginator.page(page)
        except (InvalidPage, PageNotAnInteger):
            message_s = paginator.page(1)
        except EmptyPage:
            message_s = paginator.page(paginator.num_pages)
        if message_s:
            l = []
            mess_l = []
            for message in message_s:
                username='游客'
                try:
                    username = message.user.username
                except:
                    pass
                content = message.content
                create_time = message.create_time
                create_time = create_time.strftime('%Y-%m-%d')
                comment=None
                try:
                    comment = message.comment
                except:
                    pass
                if comment:
                    com = comment.comment
                    print com
                    comment_time = comment.comment_time
                    com_time = comment_time.strftime('%Y-%m-%d')
                    l.append((('username', username), ('content', content),('total_page',str(total_page)), ('create_time', str(create_time)[0:10]),
                              ('com', com), ('comment_time', com_time)))
                else:
                    l.append((('username', username), ('content', content),('total_page',str(total_page)), ('create_time', str(str(create_time))[0:10])))
            for j in range(len(l)):
                content = dict(l[j])
                mess_l.append(content)
            con = json.dumps(mess_l)
            return HttpResponse(con,content_type='application/json')
        else:
            content = {'status': 0, 'msg': 'can not find this Type'}
            return HttpResponse(json.dumps(content),content_type='application/json')
    else:
        content = {'status': 0, 'msg': 'can not find this Type'}
        return HttpResponse(json.dumps(content),content_type='application/json')


def get_meassage(request):
    """
    获取分类
    :param request:
    :return:
    """

    return render(request,"person_lyb.html")


def message_board(request):
    '''
    留言
    :param request:
    :return:
    '''
    if request.method == 'GET':
        type_id = request.GET.get('type_id', None)
        content = request.GET.get('content',None)
        contact = request.GET.get('contact',None)
        user = request.user
        try:
            type = Messsage_Type.objects.get(type=type_id)
        except Messsage_Type.DoesNotExist:
            type = Messsage_Type.create_type(type=type_id)
        is_anonymous=user.is_anonymous()
        if is_anonymous:
            Message_Board.create_message(content, contact, type)
        else:
            Message_Board.create_message(content,contact,type,user)
        content = json.dumps([{'status':3}])
        return HttpResponse(content,content_type='application/json')
    else:
        content = json.dumps([{'status':0}])
        return HttpResponse(content,content_type='application/json')

def get_messsage_type(request):
    type_set = Messsage_Type.objects.all()
    l = []
    type_l=[]
    for type in type_set:
        type_name = type.type
        id = type.id
        l.append((('id',id),('type',type_name)))
    for j in range(len(l)):
        content = dict(l[j])
        type_l.append(content)
    con = json.dumps(type_l)
    return  HttpResponse(con,content_type='application/json')

@login_required()
def system_information(request):
    """
    系统消息
    :param request:
    :return:
    """
    user = request.user
    try:
        msg = send_message.objects.all()
        print msg,"luoxd"
    except:
        return render(request, 'person_xtxx.html')

    paginator = Paginator(msg, 5)
    page = request.GET.get('page')
    try:
        info_perpage = paginator.page(page)
    except (PageNotAnInteger,InvalidPage ):
        info_perpage = paginator.page(1)
    except EmptyPage:
        info_perpage = paginator.page(paginator.num_pages)

    return render(request, 'person_xtxx.html', {'paginator': paginator, 'info': info_perpage,'msg':msg})

#删除 系统消息
@login_required
@csrf_exempt
def delete_sysmessage(request):
    """
    删除 系统消息
    :param request:
    :param args:
    :return:
    """
    if request.method == "POST":

        id_list = request.POST.getlist('goods_check[]','')
        for i in id_list:
            messages = send_message.objects.get(id=i)

            print messages
            messages.delete()
        data = {'msg':u'删除成功','status':200}
        return HttpResponse(dumps({"data":data }))


@login_required
@csrf_exempt
def delete_collection_store(request):
    '''
    删除收藏的店铺
    :param request:
    :return:
    '''
    user = request.user
    print user
    if request.method == 'POST':
        id_list = request.POST.getlist('id[]','')
        print id_list
        for i in id_list:
            s=int(i)
            store = Store.objects.get(id=s)
            store_coll = store_collections.objects.get(store=store)
            store_coll.user.remove(user)
        msg = 'okkk'
        return JsonResponse({'msg':msg, 'status': 200})
    return JsonResponse({'msg':'not ok'})



@csrf_exempt
@login_required()
def delete_color(request):
    '''
     删除颜色
    :param request:
    :return:
    '''
    if request.method == 'POST':
        id = request.POST.get('id')

        good = goods_detal.objects.get(id=id)

        good.color = ''

        good.save()

        msg = 'success'
        return JsonResponse({'msg':msg, 'status': 200})
    return JsonResponse({'msg': 'no'})

@csrf_exempt
def complaint(request):
    """
    商品详情投诉
    :param request:
    :return:
    """
    user = request.user
    content=0
    if request.method == "POST":
        try:
            content = request.POST.get('body')
        except:
            pass
        if user.is_anonymous():
            name = u"游客"
        else:
            name = user.username
        s = Complant(name=name,body=content)
        s.save()
        return HttpResponse(dumps({"status":200}))

@csrf_exempt
def tousu(request):
    """
    投诉
    :param request:
    :return:
    """
    user = request.user
    body=0
    if request.method == "POST":
        try:
            body = request.POST.get('body')
            print body,">>>>>>>>>>>>>>>>>>>"
        except:
            return render(request, 'person_tousu.html')
    if user.is_anonymous():
        name = u"游客"
    else:
        name = user.username
    s = Complant(name = name,body=body)
    s.save()
    return render(request,'person_tousu.html')
