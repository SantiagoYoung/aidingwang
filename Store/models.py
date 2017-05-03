# -*-coding:utf-8 -*-
from django.db import models

# Create your models here.
import datetime
from django.db import models
from Accounts.models import User
from catalog.models import big_goods_type
# Create your models here.


class Store(models.Model):

    """
    店铺公司界面
    """
    #店铺
    Charaters = (
        (0, u'公司'),
        (1, u'个人'),
    )
    Status = (
        (1, u'审核中'),
        (2, u'通过'),
        (3, u'未通过'),
    )
    Kinds = (
        (0,u'生产 (包括材料提供)'),
        (1,u'设计'),
        (2,u'私人订制'),
        (3,u'工装定制'),
    )

    name = models.CharField(verbose_name=u'店铺名称', max_length=50)
    seller = models.OneToOneField(User, verbose_name=u'卖家',null=False,blank=False)
    business = models.CharField(verbose_name=u'主营',max_length=50)
    kinds = models.ForeignKey(big_goods_type,verbose_name=u'行业类型',blank=True,null=True)
    link = models.URLField(max_length=300, verbose_name=u'店铺链接', null=False)
    industry = models.IntegerField(verbose_name=u'店铺类型', choices=Kinds,default=0)
    character = models.IntegerField(verbose_name=u'行业性质', choices=Charaters, blank=True)
    phone = models.CharField(verbose_name=u'手机号码', max_length=11,help_text=u'注意填写十一位电话号码')
    QQ = models.CharField(verbose_name=u'QQ', max_length=15)
    status = models.IntegerField(verbose_name=u'店铺状态', choices=Status, default=1)
    introduction = models.TextField(verbose_name=u'店铺介绍')

    #公司
    headpicture = models.ImageField(upload_to='media',verbose_name=u'头像',blank=True,null=True)
    companyname = models.CharField(verbose_name=u'企业名称', max_length=50, null=False,blank=False)
    connectioner = models.CharField(verbose_name=u'法人',max_length=50,null=False,blank=False)
    connection_number = models.CharField(verbose_name=u'联系电话', max_length=11, null=False, blank=False)
    company_adress = models.CharField(verbose_name=u'企业地址',max_length=50,null=False,blank=False)
    company_QQ = models.CharField(verbose_name=u'企业QQ',max_length=12, null=False,blank=False)
    business_license = models.ImageField(verbose_name=u'营业执照',upload_to='media',blank=True,null=True)
    company_introduce = models.TextField(verbose_name=u'企业介绍')
    date=models.DateTimeField(verbose_name=u'入驻时间',default=datetime.datetime.now())




    class Meta:
        verbose_name = u'店铺'
        verbose_name_plural = u'店铺'

    def __unicode__(self):
        return self.name


class customer_suggestions(models.Model):
    """
    意见建议
    """
    # user = models.ForeignKey(User,verbose_name=u'用户')
    TYPE = (
        (1,u'网站建议'),
        (2,u'网站投诉'),
        (3,u'问题投诉')
            )
    date  = models.DateTimeField(auto_now_add=True,verbose_name=u'反馈时间')
    types = models.IntegerField(verbose_name=u'反馈类型',default=1)
    body = models.TextField(verbose_name=u'反馈内容')
    phone = models.IntegerField(verbose_name=u'联系方式',default=00000000000,max_length=11)
    class Meta:
        verbose_name=u'意见建议'
        verbose_name_plural=u'意见建议'



class store_collections(models.Model):
    """
    收藏店铺
    """
    store = models.OneToOneField(Store, verbose_name=u'被收藏店铺名')
    user = models.ManyToManyField(User, verbose_name=u'收藏者名')
    date = models.DateTimeField(auto_now_add=True, verbose_name=u'收藏时间')
    num = models.IntegerField(verbose_name=u'收藏数', default=0)
    class Meta:
        verbose_name = u'店铺收藏'
        verbose_name_plural = u'店铺收藏'


#系统消息
# class SysMessage(models.Model):
#
#
#     message = models.TextField(verbose_name=u'系统消息')
#     receive_user = models.ManyToManyField(User, verbose_name=u'用户')
#     pub_date = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         verbose_name_plural = u'系统信息'
#         verbose_name = u'系统信息'
#         ordering =['-pub_date']
#
#     def __unicode__(self):
#         return self.sender.username