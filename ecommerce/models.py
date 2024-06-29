from django.db import models
from django.contrib.auth.models import User


class Category_model(models.Model):
    category_name=models.CharField(max_length=100)
    category_image=models.ImageField(upload_to="images",null=True)

    def __str__(self):
        return self.category_name

class Product_model(models.Model):
    Product_name=models.CharField(max_length=100)
    product_image=models.ImageField(upload_to="images",null=True)
    product_description=models.TextField(null=True)
    product_price=models.IntegerField()
    product_stock=models.IntegerField()
    product_category=models.ForeignKey(Category_model,on_delete=models.CASCADE)


class Cart_model(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product_model,on_delete=models.CASCADE,null=True)
    total_price=models.DecimalField(decimal_places=2,max_digits=10,null=True)
    date=models.DateTimeField(auto_now_add=True,null=True)


class Order_model(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product_model,on_delete=models.CASCADE,null=True)
    order_date=models.DateTimeField(auto_now_add=True)
    address=models.CharField(max_length=1000)