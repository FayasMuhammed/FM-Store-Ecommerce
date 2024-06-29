from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,ListView,DetailView,UpdateView
from ecommerce.forms import Userregister_form,Userlogin_form,Category_form,Product_form,Orderaddress_form
from ecommerce.models import User,Category_model,Product_model,Cart_model,Order_model
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import send_mail
from django.utils.decorators import method_decorator



def signin_required(fn):
    def wrapper(request,*args,**kwrags):
        if not request.user.is_authenticated:
            return redirect("login")
        else:
            return fn(request,*args,**kwrags)
    return wrapper

def mylogin(fn):
    def wrapper(request,*args,**kwargs):
        id=kwargs.get("pk")
        data=Cart_model.objects.get(id=id)
        if data.user!=request.user:
            return redirect("login")
        else :
            return fn(request,*args,**kwargs)
    return wrapper

class Userregister_view(View):
    def get(self,request,*args,**kwargs):
        form=Userregister_form()
        return render(request,"register.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=Userregister_form(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            email=form.cleaned_data.get("email")
            password=form.cleaned_data.get("password")
            user=User.objects.create_user(username=username,email=email,password=password)


            subject="Welcome to flipstore"
            message=f'Hi, {user.username} Thank you for register in Flipstore'
            email_from=settings.EMAIL_HOST_USER
            recipient_list=[user.email,]
            send_mail(subject,message,email_from,recipient_list)
        form=Userregister_form()
        return render(request,"register.html",{"form":form})
    
class Userlogin_view(View):
    def get(self,request,*args,**kwargs):
        form=Userlogin_form()
        return render(request,"userlogin.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=Userlogin_form(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_obj=authenticate(username=u_name,password=pwd)
            if user_obj:
                login(request,user_obj)
                print("valid credentials")
            form=Userlogin_form()
            return redirect("home")
        
class Userlogout_view(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("login")
        

class Vendorregister_view(View):
    def get(self,request,*args,**kwargs):
        form=Userregister_form()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=Userregister_form(request.POST)
        if form.is_valid():
            User.objects.create_superuser(**form.cleaned_data)
            form=Userregister_form()
        return render(request,"register.html",{"form",form})
            

class Addcategory_view(CreateView):
    model=Category_model
    form_class=Category_form
    template_name="category.html"
    success_url=reverse_lazy("addcate")


class Addproduct_view(CreateView):
    model=Product_model
    form_class=Product_form
    template_name="product.html"
    success_url=reverse_lazy("add_pro")


class Categoryview_view(ListView):
    model=Category_model
    template_name='home.html'
    context_object_name='categories'


class Categorydetail_view(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        data=Product_model.objects.filter(product_category_id=id)
        return render(request,"productlist.html",{"products":data})

# its because you use the same html page for both Categorydetail_view and Productview_view you will have to use the same key name as well
# ({"products":data} and context_object_name="products") because in the html page there is only one key for both view to work.

class Productview_view(ListView):
    model=Product_model
    template_name="productlist.html"
    context_object_name="products"


class Productdetail_view(DetailView):
    model=Product_model
    template_name="productdetails.html"
    context_object_name="product_detail"


class Productupdate_view(UpdateView):
    model=Product_model
    form_class=Product_form
    template_name="product.html"
    success_url=reverse_lazy("add_pro")

@method_decorator(signin_required,name="dispatch")
class Addtocart_view(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        data=Product_model.objects.get(id=id)
        Cart_model.objects.create(user=request.user,product=data)
        c_data=Cart_model.objects.filter(user=request.user)
        price=0
        for i in c_data:
            if i.product and hasattr(i.product,"product_price"):
                price+=i.product.product_price
        return render(request,"cart.html",{"c_data":c_data,"price":price})

@method_decorator(signin_required,name="dispatch")    
class Cartlist_view(View):
    def get(self,request,*args,**kwargs):
        c_data=Cart_model.objects.filter(user=request.user)
        price=0
        count=0
        for i in c_data:
            if i.product and hasattr(i.product,"product_price"):
                price+=i.product.product_price
                count+=1
        return render(request,"cart.html",{"c_data":c_data,"price":price,"count":count})
    
@method_decorator(signin_required,name="dispatch")
@method_decorator(mylogin,name="dispatch")
class Deletecart_view(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Cart_model.objects.get(id=id).delete()
        return redirect("cartlist")
    
# class Emptycart_view(View):
#     def get(self,request,*args,**kwargs):
#         Cart_model.objects.filter().delete()
#         return redirect("cartlist")
    

class Order_view(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        data=Product_model.objects.get(id=id)
        Cart_model.objects.create(user=request.user,product=data)
        form=Orderaddress_form()
        return render(request,"order.html",{"form":form,"data":data})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        data=Product_model.objects.get(id=id)
        form=Orderaddress_form(request.POST)
        if form.is_valid():
            Order_model.objects.create(user=request.user,product=data,**form.cleaned_data)
        return render(request,"order.html",{"data":data})

@method_decorator(signin_required,name="dispatch")
class Orderlist_view(View):
    def get(self,request,*args,**kwargs):
        data=Order_model.objects.filter(user=request.user)
        return render(request,"orderlist.html",{"data":data})