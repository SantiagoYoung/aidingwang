# -*- coding: utf-8 -*-
from django import forms
from models import goods_detal

class SendGoods(forms.ModelForm):
    class Meta:
        model=goods_detal
        fields=('id','goods_name','picture','original_price','current_price','store','is_provide_design','is_provide_make',
                'is_customize_size','is_customize_patten','is_customize_style','goods_url','goods_introduce','server_introduce')

