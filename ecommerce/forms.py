from django import forms
from ecommerce.models import User,Category_model,Product_model

class Userregister_form(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password']

class Userlogin_form(forms.Form):
    username=forms.CharField(max_length=100)
    password=forms.CharField(max_length=100)


class Category_form(forms.ModelForm):
    class Meta:
        model=Category_model
        fields="__all__"


class Product_form(forms.ModelForm):
    class Meta:
        model=Product_model
        fields="__all__"


class Orderaddress_form(forms.Form):
    address=forms.CharField(max_length=100)
