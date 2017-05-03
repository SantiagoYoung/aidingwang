# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
import json


# from goods.models import Clothes, Bag, Gift, Ornament, Shoe


# from store.models import Store````````````````````````````````````````````````````````````

# Create your models here.


class MyBaseUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('The given username must be set')

        user = self.model(username=username)
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)

        user.is_admin = True

        user.save(using=self._db)

        return user



class MyBaseUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('The given username must be set')

        user = self.model(username=username)
        user.set_password(password)

        user.save(using=self._db)
        # _member = MemberInfo.objects.create(user=self)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)

        user.is_admin = True

        user.save(using=self._db)

        return user

class User(AbstractBaseUser):
    """username 是电话号码, 也是用户的唯一标志"""
    username = models.CharField(u"用户名", unique=True, max_length=30, null=False)
    is_active = models.BooleanField(u"激活", default=True)
    is_staff = models.BooleanField(u"管理员", default=False)
    is_admin = models.BooleanField(default=False, verbose_name=u'管理员')
    date_joined = models.DateTimeField(u"加入时间", default=timezone.now)
    user_advice = models.TextField(u"反馈内容",max_length=500,blank=True)
    user_question = models.TextField(u"定制问问",max_length=35,blank=True)
    contact_info = models.CharField(u"联系方式",max_length=35, blank=True)
    objects = MyBaseUserManager()
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = u"用户"
        verbose_name_plural = u"用户"

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return self.username

    def __str__(self):
        return self.username

    def has_perms(self, perm, obj=None):
        return True

    def has_perm(self, perm, obj=None):
        return True

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

class MemberInfo(models.Model):
    """店铺会员中心 -> 会员主页"""
    user = models.OneToOneField(User,verbose_name=u'用户',related_name='member',default=u'小爱')
    store_name = models.CharField(max_length=20,verbose_name=u'店铺名称',default='')
    linkman = models.CharField(max_length=20, verbose_name=u'联系人', blank=False,default='Name')
    telephone = models.CharField(max_length=20,verbose_name=u'固定电话',blank=True)
    phone_number = models.CharField(max_length=11, default='00000000000', verbose_name=u'手机')
    qq_number = models.CharField(max_length=12,verbose_name=u'QQ号',default='0000000000')
    province_adress = models.CharField(max_length=12,verbose_name=u'发货省份',blank=False,default=u'四川')
    city_adress = models.CharField(max_length=20,verbose_name=u'发货城市',blank=False,default=u'四川')
    town_adress = models.CharField(max_length=30,verbose_name=u'发货县（区）',blank=False,default=u'成都')
    send_number = models.CharField(max_length=20,verbose_name=u'邮政编码',blank=True)
    introduce_store = models.TextField(max_length=520,verbose_name=u'店铺介绍',blank=True)

    goods_collection = models.TextField(editable=True, blank=True, default=' ', verbose_name=u'收藏的商品')
    store_collection = models.TextField(editable=True, blank=True, default=' ', verbose_name=u'收藏的店铺')


    def handle_collection(self, op_type, serial_number):
        """
        保存的是店铺： id, 商品： 类型-id  (eg: Cl-12, Ba-14)...
        :param op_type: 收藏的类型 goods --> 商品， store --> 商店
        :param serial_number: 保存的是店铺： id, 商品： 类型-id  (eg: Cl-12, Ba-14)...
        :return: 2, 代表取消收藏成功  1, 代表收藏成功  False, 代表取消点赞成功  True, 代表点赞成功
        """
        try:
            if op_type == 'goods':
                content = json.loads(self.goods_collection)
            elif op_type == 'store':
                content = json.loads(self.store_collection)
            else:
                print "参数错误"
        except Exception as e:
            print e, "in accounts views.py"
            raise e
        if serial_number in content:  # 如果已经喜欢了,就删除
            content.remove(serial_number)

            if op_type == 'goods':
                self.goods_collection = json.dumps(content)

            elif op_type == 'store':
                self.store_collection = json.dumps(content)
            self.save()
            return "取消收藏成功"
        else:
            content.append(serial_number)
            content = list(set(content))
            if op_type == 'goods':
                self.goods_collection = json.dumps(content)
            elif op_type == 'store':
                self.store_collection = json.dumps(content)

            self.save()
            return "收藏成功"

    def in_collection(self, op_type, serial_number):
        """
        判断是否收藏了
        :param op_type:
        :param serial_number:
        :return:
        """
        try:
            if op_type == 'goods':
                content = json.loads(self.goods_collection)
            elif op_type == 'store':
                content = json.loads(self.store_collection)
            else:
                print "参数错误"
        except Exception as e:
            raise e
        if serial_number in content:
            return True
        else:
            return False


    def get_store_collection(self, store_obj):
        """
        返回某人收藏的店铺的List or QuerySet
        :param store_obj: 店铺的类名
        :return: List or QuerySet
        """
        content = json.loads(self.store_collection)
        collection_store = []
        for i in content:
            # 处理商品店铺被删除的情况
            try:
                collection_store.append(store_obj.objects.get(id=i))
            except Exception as e:
                print type(e)
        return collection_store

    def get_store_collection_length(self):
        """
        返回某人收藏的店铺的数量
        :return: int
        """
        content = json.loads(self.store_collection)
        le = len(content)
        return le

    def get_all_type_goods_collection(self, goods_obj_dic):
        """
        返回某人收藏的商品的List or QuerySet
        :param : goods_obj_dic， 根据字典的情况来看， 不存在的id与不需要查看的商品类型会自然地抛出异常
        :return: List or QuerySet
        """
        # print self.goods_collection
        content = json.loads(self.goods_collection)
        collection_goods = []
        for i in content:
            # 处理商品店铺被删除的情况
            try:
                collection_goods.append(goods_obj_dic[i[0:2]].objects.get(id=i[3:]))
            except Exception as e:
                print e
        return collection_goods


    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = u"用户资料"
        verbose_name_plural = u"用户资料"



class send_message(models.Model):
    """
    系统消息
    """

    # receiver = models.OneToOneField(MemberInfo,verbose_name=u'收件人')
    receiver = models.ManyToManyField(User, verbose_name=u'收件人')
    message_subject = models.CharField(verbose_name=u'消息主题',max_length=50)
    message = models.CharField(verbose_name=u'消息内容',max_length=520,blank=False)
    send_time = models.DateTimeField(auto_now_add=True,verbose_name=u'发送时间')

    def __unicode__(self):
        return self.message_subject

    class Meta:
        verbose_name = u'系统消息'
        verbose_name_plural = u'系统消息'


#*********************************************************


class Messsage_Type(models.Model):
    ''''
    留言类型
    '''
    type = models.CharField(max_length=20,verbose_name=u'留言类型')
    class Meta:
        verbose_name=u'留言类型'
        verbose_name_plural=u'留言类型'
    def __unicode__(self):
        return self.type

    @classmethod
    def get_all_type(cls):
        type_set = cls.objects.all()
        return type_set

    @classmethod
    def create_type(cls,type):
        new_type = cls.objects.create(type=type)
        new_type.save()
        return new_type

    @classmethod
    def delete_type(cls, type_id):
        try:
            type=cls.objects.get(type_id)
        except Messsage_Type.DoesNotExist:
            return {'status':0,'msg':'没有这个类型'}
        type.delete()
        return {'status':1,'msg':'sucess'}

    @classmethod
    def change_type(cls,type_id,type):
        try:
            type_n = cls.objects.get(type_id)
        except Messsage_Type.DoesNotExist:
            return {'status': 0, 'msg': '没有这个类型'}
        type_n.type =type
        return {'status': 1, 'msg': 'sucess'}

class Message_Comment(models.Model):
    '''
    留言板回复
    '''
    comment = models.TextField(verbose_name=u'回复', blank=True, null=True)
    comment_time = models.DateTimeField(verbose_name=u'回复时间',default=timezone.now())

    class Meta:
        verbose_name=u'留言回复'
        verbose_name_plural=u'留言回复'
    # def __unicode__(self):
    #     return str(self.message.user)


class Message_Board(models.Model):
    """
    留言板
    """
    STICK=(
        (0,u'置顶顺序1'),
        (1,u'置顶顺序2'),
        (2, u'置顶顺序3'),
        (3, u'置顶顺序4'),
        (4, u'置顶顺序5'),
        (5, u'置顶顺序6')
    )
    STATUS=(
        (0,u'审核通过可以展示'),
        (1,u'审核未通过暂不展示')
    )
    stick = models.IntegerField(choices=STICK,verbose_name=u'一键置顶',default=7,null=True,blank=True,help_text=u'请注意置顶信息只能置顶6条')
    status=models.IntegerField(choices=STATUS,verbose_name=u'是否展示',default=1,null=True,blank=True,help_text=u'后台管理员自己确定留言是否展示')
    type = models.ForeignKey(Messsage_Type,verbose_name=u'留言类型')
    user = models.ForeignKey(User,verbose_name=u'留言者',blank=True,null=True)
    contact =  models.CharField(max_length=25,verbose_name=u'联系方式',blank=True,null=True)
    content = models.TextField(verbose_name=u'内容')
    create_time = models.DateTimeField(verbose_name=u'留言时间',default=timezone.now())
    comment = models.ForeignKey(Message_Comment,verbose_name=u'回复',blank=True,null=True)
    class Meta:
        verbose_name=u'留言板'
        verbose_name_plural=u'留言板'
    def __unicode__(self):
        return self.contact
    @classmethod
    def get_message(cls,type):
        if type == None or type == '':
            message_set = cls.objects.filter(type_id=1)
            if message_set:
                return message_set
            else:
                message_set = None
                return  message_set
                # return  {'status':0}
        else:
            message_set = cls.objects.filter(type = type)
            if message_set:
                return  message_set
            else:
                message_set = None
                return message_set
                # return {'status':0}

    @classmethod
    def create_message(cls,content,contact,type,user=None):
        if user != None and user != '' and user.is_active:
            message = cls.objects.create(content = content,contact=contact,type=type,user=user)
        else:
            message = cls.objects.create(content=content, contact=contact, type=type)
        return {'status':1,'msg':'sucess'}


class Complant(models.Model):
    """
    投诉信息
    """
    name = models.CharField(verbose_name=u'投诉人',max_length=30)
    body = models.TextField(verbose_name=u'投诉内容')
    date= models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u'投诉信息'
        verbose_name_plural = u'投诉信息'
    def __unicode__(self):
        return self.name





