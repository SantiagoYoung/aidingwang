# # -*- coding: utf-8 -*-
# from Garments.models import Women_clothes_made,Man_clothes_made
# from Garments.models import sons_clothes_made,hunsha_clothes_made,qipao_clothes_made,lover_clother_made
# from Accessories.models import Gentleman_bags,Lady_bags,Gentleman_shoes,Lady_shoes, Ornaments, Ties
# from Exquisite_baubles.models import Creative, Festival, Craft, Birthday
# from Working_clothes.models import Cleaner_clothes, Guide_clothes, Actor_clothes, Labor_clothes, Profession_clothes, Hotel_clothes, Doctor_clothes, Security_clothes
from random import random,randint,Random
import re




def check_email(email):

    if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
        return email

def check_eight_goods(list):
       """
       用于判断商品是否大于8
       :param list:
       :return:
       """
       if len(list) >=8:
              num = 8
       else:
              num = len(list)
       return num
def return_hot_eights_goods(obj):
       """
       返回最新的八个商品
       :param obj:
       :return:
       """
       goods_lists = obj.objects.all().filter(is_active=True)
       num =check_eight_goods(goods_lists)
       goods_lists = list(goods_lists)
       goods_lists.reverse()
       goods_lists = sorted(goods_lists)[:num]
       return goods_lists



def get_code():
    TOTAL = '0123456789'
    TOTAL_LENGTH = len(TOTAL)
    CODE_LENGTH = 6
    random = Random()
    verification = ''
    for i in range(CODE_LENGTH):
        verification += TOTAL[random.randint(0, TOTAL_LENGTH - 1)]
    return verification