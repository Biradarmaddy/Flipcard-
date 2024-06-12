from django.contrib import admin

from .models import Products, ProductsCategory, ProductImages, ProductReviewsRatings, ProductInteraction

# Register your models here.

admin.site.register(Products)
admin.site.register(ProductInteraction)
admin.site.register(ProductsCategory)
admin.site.register(ProductReviewsRatings)
admin.site.register(ProductImages)

