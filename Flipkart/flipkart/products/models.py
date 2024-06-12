from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Products(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    product_name = models.CharField(max_length=256)
    product_description = models.CharField(max_length=256)
    brand = models.CharField(max_length=256)
    price = models.IntegerField()
    stock_quantity = models.IntegerField()
    sku = models.CharField(max_length=256)


class ProductsCategory(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    category = models.CharField(max_length=256)
    subcategory1 = models.CharField(max_length=256)
    subcategory2 = models.CharField(max_length=256)


class ProductImages(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="prod_images/", null=True)


class TagsKeywords(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=256)


class ProductReviewsRatings(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    review = models.TextField(blank=True)
    rating = models.FloatField()


class ProductInteraction(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
