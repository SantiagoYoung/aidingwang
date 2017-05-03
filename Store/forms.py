from models import Store,customer_suggestions
from django import forms


class StoreForm(forms.ModelForm):
    QQ = forms.CharField(max_length=11, min_length=5,widget=forms.TextInput())
    company_QQ = forms.CharField(max_length=11, min_length=5,widget=forms.TextInput())
    class Meta:
        model = Store
        fields= ['name','business','kinds','link','industry','character','phone','QQ','introduction','headpicture','companyname','connectioner','connection_number','company_adress','company_QQ','business_license','company_introduce']


def __init__(self, *args, **kwargs):
    super(StoreForm, self).__init__(*args, **kwargs)

    for fieldname in self.base_fields:
        field = self.base_fields[fieldname]
        field.widget.attrs.update({'class ':'form - control'})

class Customer_suggestionsForm(forms.ModelForm):
    class Meta:
        model = customer_suggestions
        fields = ['types','body','phone']