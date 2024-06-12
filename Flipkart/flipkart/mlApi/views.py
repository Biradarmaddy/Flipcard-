from django.shortcuts import render,get_object_or_404,HttpResponse
import numpy as np
import random
from django.http import JsonResponse
from sklearn.decomposition import NMF
from django.contrib.auth.models import User
from products.models import Products,ProductInteraction,ProductReviewsRatings,ProductImages,ProductsCategory,TagsKeywords
from .demo_model import counsel
# Create your views here.

# Utility Functions
def recommend_products_algo(products, user_item_matrix, user_index, num_recommendations=5):
    model = NMF(n_components=2)  # Adjust the number of components as needed
    W = model.fit_transform(user_item_matrix)
    H = model.components_

    user_preferences = W[user_index, :]
    predicted_ratings = np.dot(user_preferences, H)

    # Get indices of top N recommended products
    recommended_indices = predicted_ratings.argsort()[-num_recommendations:][::-1]
    print(products)
    print(recommended_indices)

    recommended_products = [products[i] for i in recommended_indices]
    random.shuffle(recommended_products)
    return recommended_products

def gatherData(products):
    allProducts = []
    for product in products:
        try:
            try:
                prodCat = get_object_or_404(ProductsCategory,product=product)
            except:
                prodCat = {
                        "subcategory1":"",
                        "subcategory2":"",
                        "category":"",
                        }
                prodCat = ProductsCategory()
            try:
                tags = get_object_or_404(TagsKeywords,product=product)
            except:
                tags={
                        "tags":""
                }
                tags = TagsKeywords()
            try:
                rating = get_object_or_404(ProductReviewsRatings,product=product)
            except:
                rating={

                    "rating":"",
                    "review": ""
                 }
                rating = ProductReviewsRatings()

            images = list(ProductImages.objects.filter(product=product))


            img_list = [i.image.url for i in images]
            data = {
                # "clicks": recommended_indices.i,
                "id": product.id,
                "product_name": product.product_name,
                "product_description": product.product_description,
                "brand": product.brand,
                "price": product.price,
                "stock_quantity": product.stock_quantity,
                "sku": product.sku,
                "category": prodCat.category,
                "subcategory1": prodCat.subcategory1,
                "subcategory2": prodCat.subcategory2,
                "review": rating.review,
                "rating": rating.rating,
                "tags": tags.keyword,
                "images":img_list
            }
            allProducts.append(data)
        except:
            continue


    return allProducts


def recommendProducts(request,pk):
    cuser = get_object_or_404(User,pk=pk)
    productsInteraction = []

    allUsers = User.objects.all()

    prods = Products.objects.all()
    i = 0
    current_user_index = -1
    for user in allUsers:
        prodInteraction = []
        if user == cuser:
            current_user_index = i
        for prod in prods:
            prodInteraction.append(len(ProductInteraction.objects.filter(user=user,product=prod)))
        productsInteraction.append(prodInteraction)
        i+=1

    recommended_products = recommend_products_algo(list(prods),productsInteraction,current_user_index,10)
    recommendProducts_2 = counsel(list(prods),productsInteraction,current_user_index,10)
    recommended_products = list(set(recommended_products+recommendProducts_2))
    recommended_products = gatherData(recommended_products)
    random.shuffle(recommended_products)

    return JsonResponse({"data":recommended_products})






