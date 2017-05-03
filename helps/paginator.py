# -*- coding: utf-8 -*-
from django.core.paginator import Paginator,EmptyPage,InvalidPage,PageNotAnInteger

def Getpag(request,list,page_nums,after_range_num,bevor_range_num):
    """
    分页处理
    :param request:
    :param objects_list:queryset查询集
    :param after_range_num: ->当前页前显示几页
    :param bevor_range_num: ->当前页后显示几页
    :param page_nums: 每页显示多少个
    :return:
    """
    paginator = Paginator(list, page_nums)  # list，是传过来的查好的数据

    sum_page = paginator.num_pages  # 获得当前数据总共分页的页数

    try:

        page = int(request.GET.get('page'))

    except:

        page = 1

        if page < 1:

            page=1

    try:

        list = paginator.page(page)

    except (PageNotAnInteger,InvalidPage):

        list = paginator.page(1)  # 页码不是整数,返回第一页

    except EmptyPage:

        list = paginator.page(paginator.num_pages)

    if page > after_range_num:

        page_range = paginator.page_range[page - after_range_num:page + bevor_range_num]  # 用到的是range函数

    if page > sum_page - bevor_range_num:

        page_range = paginator.page_range[
                 sum_page - after_range_num - bevor_range_num:page + sum_page]  # 这个if判断是为了，当点击最后两页的页数跳转时，页面只显示3个，如果加了判断的话，会显示五页

    else:

        page_range = paginator.page_range[0:after_range_num + bevor_range_num + 1]

    content = {

        'list': list,

        'page_range': page_range

    }

    return content