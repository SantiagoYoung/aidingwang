# # -*- coding: utf-8 -*-
# from django import forms
# # from help.type import CLOTHES, BAG, SHOE, ORNAMENT, GIFT
# # from store.models import Store
# #
# #
# # class WriteForm(forms.Form):
# #     pic = forms.ImageField(label='image:')
# #     k = forms.BooleanField()
# #     n = forms.ModelMultipleChoiceField(queryset=Store.objects.all())
# #
# #
# # class GoodsForm(forms.Form):
# #     """上传商品的表单"""
# #     goods_name = forms.CharField(label='商品名')
# #     original_price = forms.FloatField(label=u'原价')
# #     current_price = forms.FloatField(label=u'现价')
# #     is_provide_design = forms.BooleanField(label=u'提供设计')
# #     is_provide_make = forms.BooleanField(label=u'提供制作')
# #     goods_url = forms.URLField(max_length=300, label=u'商品链接')
# #
# #     goods_description = forms.Textarea()
# #     goods_description_image = forms.ImageField(label=u'图片描述')
# #
# #     service_description = forms.Textarea()
# #     service_description_image = forms.ImageField(label=u'图片描述')
# #
# #     # interest = forms.MultipleChoiceField(choices=CLOTHES)
# #     clothes = forms.ChoiceField(choices=CLOTHES, widget=forms.RadioSelect(), label='服装')
# #     bag = forms.ChoiceField(choices=BAG, widget=forms.RadioSelect(), label='包')
# #     shoe = forms.ChoiceField(choices=SHOE, widget=forms.RadioSelect(), label='鞋子')
# #     ornament = forms.ChoiceField(choices=ORNAMENT, widget=forms.RadioSelect(), label='配饰')
# #     gift = forms.ChoiceField(choices=GIFT, widget=forms.RadioSelect(), label='礼品')
# #
# #
# # class RegisterForm(forms.Form):
# #     # sellername = forms.CharField(label='店名:', max_length=100)
# #     password = forms.CharField(label='密码', widget=forms.PasswordInput)
# #     password2 = forms.CharField(label='Confirm', widget=forms.PasswordInput)
# #     email = forms.IntegerField(label='邮箱:')
# #
# #     def pwd_validate(self, p1, p2):
# #         return p1 == p2
# #
# #
# class LoginForm(forms.Form):
#     username = forms.CharField(label='邮箱：', widget=forms.TextInput(attrs={'id': "email"}))
#     password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'id': "password"}))
#
#
