from django.urls import path
from ecommerce.views import *



urlpatterns=[
    path('reg/',Userregister_view.as_view(),name="reg"),
    path('log/',Userlogin_view.as_view(),name="login"),
    path('logout/',Userlogout_view.as_view(),name="logout"),
    path('vreg/',Vendorregister_view.as_view(),name="vreg"),
    path('addcate/',Addcategory_view.as_view(),name="addcate"),
    path('add_pro/',Addproduct_view.as_view(),name="add_pro"),
    path('home/',Categoryview_view.as_view(),name="home"),
    path('listp/',Productview_view.as_view(),name="listp"),
    path("detailp/<int:pk>",Productdetail_view.as_view(),name="detailp"),
    path("updatep/<int:pk>",Productupdate_view.as_view(),name="updatep"),
    path('productd/<int:pk>',Categorydetail_view.as_view(),name="productd"),
    path('add_cart/<int:pk>',Addtocart_view.as_view(),name="add_cart"),
    path('deletec/<int:pk>',Deletecart_view.as_view(),name="deletec"),
    path('cartlist/',Cartlist_view.as_view(),name="cartlist"),
    path('order/<int:pk>',Order_view.as_view(),name="order"),
    path('orderlist/',Orderlist_view.as_view(),name="orderl"),
    # path('emp/',Emptycart_view.as_view(),name="emptyc"),      

]