from django.shortcuts import render,get_object_or_404,HttpResponse
import numpy as np
from django.http import JsonResponse
from sklearn.decomposition import NMF
from django.contrib.auth.models import User
from products.models import Products,ProductInteraction,ProductReviewsRatings,ProductImages,ProductsCategory,TagsKeywords



def counsel(products, UTM, UI, num_recommendations=5):
    model = NMF(n_components=2)  
    W = model.fit_transform(UTM)
    H = model.components_

    choices = W[UI, :]
    predicted_ratings = np.dot(choices, H)

    
    recommended_indices = predicted_ratings.argsort()[-num_recommendations:][::-1]
    print(products)
    print(recommended_indices)

    recommended_products = [products[i] for i in recommended_indices]
    return recommended_products
