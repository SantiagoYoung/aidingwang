# -*- coding:utf-8 -*-
import httplib
import urllib
import time
import os
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from json import dumps
import uuid
from PIL import ImageFile
from datetime import date, datetime,time
from PIL import Image, ImageFilter


def user_check(user):
    #后台管理员权限设置
	return not user.is_superuser



def json_response(results=[], status=200, message=None):
    """
    # 相对于普通的json_response多了一个处理datetime 对象的过程
    :param results:
    :param status:
    :param message:
    :return:
    """

    return HttpResponse(dumps({
        'results': results,
        'status': status,
        'message': message,
    }))


def json_response_with_time(results=[], status=200, message=None):
    """
    相对于普通的json_response多了一个处理datetime 对象的过程
    :param results:
    :param status:
    :param message:
    :return:
    """
    for i in results:
        _time = i["time"]
        _time = __default_time(_time)
        i["time"] = _time
    return HttpResponse(dumps({
        'results': results,
        'status': status,
        'message': message,
    }))


def __default_time(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')
    elif isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    else:
        raise TypeError('%r is not JSON serializable' % obj)


def my_store_required(view_func):
    """需要有店铺"""

    def _wrap_view(request, *args, **kwargs):
        # 若没开店铺, request.user.store_set.all() 会是空字符串
        if request.user.store_set.all():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/store/safepersonal/0/")

    return _wrap_view


def my_member_required(view_func):
    """需要填写个人详细信息"""

    def _wrap_view(request, *args, **kwargs):
        try:
            u = request.user.member
            return view_func(request, *args, **kwargs)
        except Exception as e:
            print e, "member in utils.py"
            return HttpResponseRedirect("/store/safepersonal/1/")

    return _wrap_view


def my_admin_required(view_func):
    """管理员权限"""

    def _wrap_view(request, *args, **kwargs):
        if request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/accounts/404/")

    return _wrap_view

def paginator(request, obj_or_list, page_size=10, after_range_num=5, before_range_num=6):
    """
    用于分页
    :usage eg: page_objects, page_range = paginator(request, store)
    :param request:
    :param obj_or_list: type -> QuerySet or list
    :param page_size: 每页最大数量
    :param after_range_num:
    :param before_range_num: 决定最多显示多少页码
    :return: page_objects -> 分页对象,  page_range -> 页
    """
    try:
        page = int(request.GET.get("page", 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    paginator = Paginator(obj_or_list, page_size)
    try:
        pa = paginator.page(page)
    except(EmptyPage, InvalidPage, PageNotAnInteger):
        pa = paginator.page(1)
    if page >= after_range_num:
        page_range = paginator.page_range[page - after_range_num:page + before_range_num]
    else:
        page_range = paginator.page_range[0:int(page) + before_range_num]
    page_objects = pa
    return page_objects, page_range


def upload_image(_file, path="/business_licence/%Y/%m/%d/"):
    """
    图片上传函数
    :param _file:
    :param path: eg: "/business_licence/%Y/%m/%d/"
    :return:
    """
    if _file:
        path = os.path.join(settings.MEDIA_ROOT + path, 'upload')
        file_name = str(uuid.uuid1()) + ".jpg"
        path_file = os.path.join(path, file_name)
        parser = ImageFile.Parser()
        for chunk in _file.chunks():
            parser.feed(chunk)
        img = parser.close()
        try:
            if img.mode != "RGB":
                img = img.convert("RGB")
            img.save(path_file, 'jpeg', quality=100)
        except Exception as e:
            return False
        return True
    return False


def create_image(imgfile, obj):
    """
    创建图片
    :param img: 上传图片
    :param obj: 创建的图片对象， 细节的or整体的
    :return: 创建的图片对象
    """
    img = obj.objects.create(image=imgfile)
    img.name = str(uuid.uuid1())
    img.save()
    return img


def check_upgoods_param(type_list, url_address, goods_pre_price, goods_price, goods_texture, goods_season, goods_model,
                        total_show_list, detail_show_list, goods_description, goods_descrippic,
                        service_note, service_notepic):
    """
    上传商品的参数检查
    :param request:
    :param type_list:
    :param url_address:
    :param goods_pre_price:
    :param goods_price:
    :param goods_texture:
    :param goods_season:
    :param goods_model:
    :param total_show_list:
    :param detail_show_list:
    :param goods_description:
    :param goods_descrippic:
    :param service_note:
    :param service_notepic:
    :return:
    """
    # 参数检查
    # 至少一个， 最多两个
    if not (len(type_list) == 1 or len(type_list) == 2):
        results = ["check_box_list"],
        status = 400,
        message = "请选择分类， 1~2个"
        return results, status, message

    # if "www" not in url_address:
    #     return

    try:
        float(goods_pre_price)
        float(goods_price)
    except ValueError as e:
        print e, "store views.py"

        results = [1],
        status = 400,
        message = "价格输入错误"
        return results, status, message

    # 参数检查
    # 宝贝材质请填写完整
    if not (goods_texture and goods_season and goods_model):
        print "孔令星"

        results = [2],
        status = 400,
        message = "宝贝材质请填写完整"
        return results, status, message

    # 参数检查
    # total_show_list, detail_show_list 没传图片的时候是空列表 type --> List
    if not (total_show_list and detail_show_list):
        results = [3],
        status = 400,
        message = "请上传图片"
        return results, status, message

    # 参数检查
    if not (goods_description or goods_descrippic):
        results = ["goods_description"],
        status = 400,
        message = "文字描述与图片描述至少有一个"
        return results, status, message

    # 参数检查
    if not (service_note or service_notepic):
        results = ["service_note"],
        status = 400,
        message = "文字描述与图片描述至少有一个"
        return results, status, message
    results = [""]
    status = 200
    message = "可以"
    return results, status, message
