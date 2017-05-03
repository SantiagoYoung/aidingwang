# -*- coding: utf-8 -*-
from Accounts.models import User
from django.db import models
from ckeditor.fields import RichTextField
from Accounts.models import User,MemberInfo
import datetime


# Create your models here.

class big_goods_type(models.Model):
    """
    商品大分类模型
    """
    name = models.CharField(verbose_name=u'商品大类名称',help_text=u'商品大分类的选项',max_length=120)
    big_picture1 = models.ImageField(upload_to='Pic',verbose_name=u'大类图标',help_text=u'大类展示图1',null=False,blank=False)
    big_picture2 = models.ImageField(upload_to='Pic', verbose_name=u'大类图标', help_text=u'大类展示图2', null=False, blank=False)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')
    update = models.DateTimeField(auto_now=True,verbose_name=u'修改时间')
    class Meta:
        ordering = ['-create_time']
        verbose_name = u'商品大类名称'
        verbose_name_plural = u'商品大类名称'

    def __unicode__(self):
        return self.name


class small_goods_type(models.Model):
    """
    商品小分类模型
    """
    name = models.CharField(verbose_name=u'商品小分类名称', help_text=u'商品小分类的选项', max_length=120)
    belong_to_big = models.ForeignKey(big_goods_type,verbose_name=u'所属大分类',related_name='small')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')

    class Meta:
        ordering = ['-create_time']
        verbose_name = u'商品小类名称'
        verbose_name_plural = u'商品小类名称'

    def __unicode__(self):
        return self.name

class goods_detal(models.Model):
    """
    商品详情模型
    """
    INDEX= (
        (0,u'不在首页展示'),
        (1,u'在首页展示')
    )
    CHOICE = (
        (0, u'按商品详情展示'),
        (1, u'按大类列表展示'),
    )
    TYPE = (
        (0, u'审核中'),
        (1, u'未通过'),
        (2, u'审核通过'),
        (3, u'已过期')

    )
    show_index = models.BooleanField(verbose_name=u'是否首页展示',choices=INDEX,default=0,help_text=u'注意:每个大类只能展示八个商品')
    goods_name = models.CharField(max_length=35, verbose_name=u'商品名', default=u'未命名商品')
    belong_to_big = models.ForeignKey(big_goods_type,verbose_name=u'所属大分类')
    belong_to_small = models.ForeignKey(small_goods_type,verbose_name=u'所属小分类')
    status = models.IntegerField(verbose_name=u'商品审核',choices=TYPE ,default=0)
    type = models.IntegerField(choices=CHOICE,verbose_name=u'选择展示内容',default=0)
    picture = models.ImageField(upload_to='Pic', blank=True, null=True, verbose_name=u'展示图片')
    original_price = models.CharField(verbose_name=u'原价', default=0.0,max_length=10)
    current_price = models.CharField(verbose_name=u'现价', default=0.0,max_length=10)
    seller = models.ForeignKey(User,verbose_name=u'卖家',null=True,blank=True)
    store = models.CharField(verbose_name=u'店铺名称',max_length=60,null=True,blank=True)
    is_provide_design = models.BooleanField(default=False, verbose_name=u'提供设计')
    is_provide_make = models.BooleanField(default=False, verbose_name=u'提供制作')

    color = models.CharField(max_length=520, verbose_name=u'商品颜色', default=u'无')

    is_customize_size = models.BooleanField(default=False, verbose_name=u'定制尺码')
    is_customize_patten = models.BooleanField(default=False, verbose_name=u'定制图案')
    is_customize_style = models.BooleanField(default=False, verbose_name=u'定制款式')
    inventory = models.IntegerField(default=0, blank=True, verbose_name=u'库存')
    goods_url = models.URLField(max_length=300, verbose_name=u'商品链接', blank=False, null=True)
    like_number = models.IntegerField(default=0, blank=True, null=True, verbose_name=u'被收藏数')
    date = models.DateTimeField(auto_now=True, verbose_name=u'发布时期')
    goods_introduce = models.TextField(verbose_name=u'商品介绍')
    server_introduce = models.TextField(verbose_name=u'服务说明')


    class Meta:
        ordering = ['-date']
        verbose_name = u'商品详情'
        verbose_name_plural = u'商品详情'

    def __unicode__(self):
        return self.goods_name

    def sale_price(self):
        if self.original_price > self.current_price:
            return self.current_price
        else:
            return None




class GoodsPicture(models.Model):
    """
    商品图图片
    """
    # TYPE=(
    #     (0, u'整体款式'),
    #     (1,u'细节做工')
    # )
    # LXDLHL
    goods = models.ForeignKey(goods_detal,verbose_name=u'所属商品',related_name='detail_picture')
    picture_id = models.IntegerField(verbose_name=u'商品显示顺序')
    picture = models.ImageField(verbose_name=u'商品详情图片',upload_to='Pic',blank=True,null=True)
    date = models.DateTimeField(auto_now=True,verbose_name=u'上传时间')
    class Meta:
        verbose_name=u'整体款式图片'
        verbose_name_plural=u'整体款式图片'
    def __unicode__(self):
        return str(self.goods_id)


class GoodsDetailPicture(models.Model):
    """
    细节做工图片
    """
    good = models.ForeignKey(goods_detal,verbose_name=u'所属商品',related_name='pictures')
    picture_detail = models.ImageField(verbose_name=u'商品详情图片',upload_to='Pic',blank=True,null=True)
    date = models.DateTimeField(auto_now=True,verbose_name=u'上传时间')
    class Meta:
        verbose_name=u'细节做工图片'
        verbose_name_plural=u'细节做工图片'
    def __unicode__(self):
        return str(self.good_id)




class goods_coments(models.Model):
    """
    商品评论
    """
    user = models.OneToOneField(User,verbose_name=u'用户名')
    goods = models.OneToOneField(goods_detal,verbose_name=u'评论商品')
    date = models.DateTimeField(auto_now_add=True,verbose_name=u'评论时间')
    coments = models.TextField(verbose_name=u'评论内容',default='')
    class Meta:
        verbose_name=u'商品评论'
        verbose_name_plural=u'商品评论'
    def __unicode__(self):
        return self.user


class send_example(models.Model):
    """
    上传商品实例
    """
    title = models.CharField(verbose_name=u'主题',max_length=20,default='')
    body = RichTextField(config_name='default', null=True, blank=True, verbose_name=u'内容')
    date = models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')
    class Meta:
        verbose_name = u'上传示例'
        verbose_name_plural = u'上传示例'
    def __unicode__(self):
        return self.title

class Lunbotu(models.Model):
    """
    主页轮播图
    """
    picture = models.ImageField(upload_to='Lunbotu',verbose_name=u'轮播图',blank=False,null=False)
    date = models.DateTimeField(auto_now_add=True, verbose_name=u'发布时期')
    class Meta:
        verbose_name=u'轮播图'
        verbose_name_plural=u'轮播图'
    def __unicode__(self):
        return str(self.date)


class IndexPicture(models.Model):
    """
    首页头部四张图片展示
    """
    index_picture = models.ImageField(upload_to='Pic',verbose_name=u'首页头部图片展示',help_text=u'管理员必填,请只填四张')
    date = models.DateTimeField(auto_now=True,verbose_name=u'上传时间')


    class Meta:
        verbose_name=u'首页头部展示图片'
        verbose_name_plural=u'首页头部展示图片'
    def __unicode__(self):
        return str(self.date)


class goods_collections(models.Model):
    """
    收藏商品
    """

    goods = models.ForeignKey(goods_detal, verbose_name=u'被收藏商品名')
    user = models.ManyToManyField(User,verbose_name=u'收藏者')
    date = models.DateTimeField(auto_now_add=True,verbose_name=u'收藏时间',default=datetime.datetime.now())
    num = models.IntegerField(verbose_name=u'被收藏数',default=0)
    class Meta:
        verbose_name=u'商品收藏'
        verbose_name_plural=u'商品收藏'
    def __unicode__(self):
        return str(self.date )

