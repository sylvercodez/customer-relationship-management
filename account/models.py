from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Customers(models.Model):
    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
    Name = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True) 
    email = models.CharField(max_length=200,null=True) 
    profile_pic = models.ImageField(default="profilepic.png",null=True,blank=True)
    date_created =models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.Name



class Tags(models.Model):
    Name = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.Name

class Products(models.Model):
    CATEGORY = (
        ('indoor','indoor'),
        ('outdoor','outdoor'),
    )
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField(max_length=200,null=True)
    category = models.CharField(max_length=200,null=True,choices=CATEGORY)
    description = models.CharField(max_length=200,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    tags = models.ManyToManyField(Tags)
    def __str__(self):
        return self.name

class Orders(models.Model):
    STATUS = (
        ('pending','pending'),
        ('out_of_delivery','out_of_delivery'),
        ('delivered','delivered'),
        )
    customer = models.ForeignKey(Customers,null=True,on_delete=models.SET_NULL)
    product = models.ForeignKey(Products, null= True,on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    status = models.CharField(max_length=200,null=True, choices=STATUS) 
    note = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.product.name