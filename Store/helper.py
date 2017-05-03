# -*-coding:utf-8 -*-


# 判断手机号是否正确
def check_phone_num(num):
    num = num.replace(' ', '')
    return num.isdigit() and len(num) == 11 and num[0] == '1'
