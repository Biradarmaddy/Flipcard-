import random

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404,render
import matplotlib.pyplot as plt
from django.db.models import Avg
from io import BytesIO
import seaborn as sns

from .models import Products, ProductsCategory, ProductImages, TagsKeywords, ProductReviewsRatings, ProductInteraction


# Create your views here.
# Util functions

def getSingleProdct(request,id):
    product = get_object_or_404(Products,id=id)
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
    try:
        # images = get_object_or_404(ProductImages, product=product)
        # img_list = [i.image for i in images]
        images = list(ProductImages.objects.filter(product=product))
        img_list = [i.image.url for i in images]
    except:
        images = []
        img_list = []

    data = {
        "id":product.id,
        "product_name":product.product_name,
        "product_description":product.product_description,
        "brand":product.brand,
        "price":product.price,
        "stock_quantity":product.stock_quantity,
        "sku":product.sku,
        "category":prodCat.category,
        "subcategory1":prodCat.subcategory1,
        "subcategory2":prodCat.subcategory2,
        "review":rating.review,
        "rating":rating.rating,
        "tags":tags.keyword,
        "images":img_list
    }
    return JsonResponse(data)

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

def getAll(request):
    a = Products.objects.all()
    return JsonResponse( {"data":gatherData(a)})

def getCategoryProducts(request,cat):
    prodCat = ProductsCategory.objects.filter(category=cat)
    allProds = []
    for i in prodCat:
        product = i.product

        # tags = get_object_or_404(TagsKeywords, product=product)
        # rating = get_object_or_404(ProductReviewsRatings, product=product)
        try:
            images = ProductImages.oject.filter(product=product)
        except:
            images = []
        img_list = [i.image for i in images]
        data = {
            "id": product.id,
            "product_name": product.product_name,
            "product_description": product.product_description,
            "brand": product.brand,
            "price": product.price,
            "stock_quantity": product.stock_quantity,
            "sku": product.sku,
            "category": i.category,
            "subcategory1": i.subcategory1,
            "subcategory2": i.subcategory2,
            "review": [],
            "rating": [],
            "tags": [],
            "images":img_list
        }
        allProds.append(data)
        random.shuffle(allProds)
    return HttpResponse(str({"data":allProds}))


def getIncrement(request,pid,uid):
    if request.method == "GET":
         prod = get_object_or_404(User,pk=uid)
         uid = get_object_or_404(Products,id=pid)
         incremented_product = ProductInteraction()
         incremented_product.product = uid
         incremented_product.user = prod
         incremented_product.save()
         return JsonResponse({"result":"incremented"})
    return JsonResponse({"result":"Invalid Request"})



def search(request,keyword):
    products = TagsKeywords.objects.filter(keyword=keyword)
    searchResults = []
    for i in products:
        product = i.product
        prodCat = get_object_or_404(ProductsCategory, product=product)
        rating = get_object_or_404(ProductReviewsRatings, product=product)
        try:
            images = get_object_or_404(ProductImages, product=product)
        except:
            images = []
        img_list = [i.image for i in images]
        data = {
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
            "tags": i.keyword,
            "images":img_list
        }
        searchResults.append(data)
    return HttpResponse(str({"data":searchResults}))


def top_product(request):
    # Fetching the top 5 products based on average ratings
    top_products = Products.objects.annotate(avg_rating=Avg('productreviewsratings__rating')).order_by('-avg_rating')[:5]

    product_names = [product.product_name for product in top_products]
    avg_ratings = [product.avg_rating for product in top_products]

    # Creating a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(product_names, avg_ratings, color='skyblue')
    plt.xlabel('Product Names')
    plt.ylabel('Average Ratings')
    plt.title('Top 5 Products by Average Ratings')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Saving the chart to a file
    chart_path = 'C:\\Users\\Dell\\Downloads\\Code Zip1\\Code Zip\\Backend\\Flipkart\\Flipkart\\flipkart\\products\\graphs\\graph.png'
    plt.savefig(chart_path)

    # Closing the plot
    plt.close()

    # Sending the chart path along with the data to the template
    data = {
        'product_names': product_names,
        'avg_ratings': avg_ratings,
        'chart_path': chart_path,
    }
    return render(request, 'top_products.html', data)


def top_products(request):
    # Fetching the top 5 products based on average ratings
    top_products = Products.objects.annotate(avg_rating=Avg('productreviewsratings__rating')).order_by('-avg_rating')[:5]

    product_names = [product.product_name for product in top_products]
    avg_ratings = [product.avg_rating for product in top_products]

    # Creating a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(product_names, avg_ratings, color='skyblue')
    plt.xlabel('Product Names')
    plt.ylabel('Average Ratings')
    plt.title('Top 5 Products by Average Ratings')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Saving the chart to a file
    chart_path = 'C:\\Users\\Dell\\Downloads\\Code Zip1\\Code Zip\\Backend\\Flipkart\\Flipkart\\flipkart\\products\\graphs\\graph.png'
    plt.savefig(chart_path)

    # Closing the plot
    plt.close()

    # Sending the chart path along with the data to the template
    data = {
        'product_names': product_names,
        'avg_ratings': avg_ratings,
        'chart_path': chart_path,
    }
    return JsonResponse(data)



def pie_chart(request):
    # Retrieve all unique categories
    categories = ProductsCategory.objects.values_list('category', flat=True).distinct()

    # Count the number of products in each category
    category_counts = {}
    total_products = 0
    for category in categories:
        count = ProductsCategory.objects.filter(category=category).count()
        category_counts[category] = count
        total_products += count

    # Calculate percentages
    category_percentages = {category: (count / total_products) * 100 for category, count in category_counts.items()}

    # Plotting the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(category_percentages.values(), labels=category_percentages.keys(), autopct='%1.1f%%')
    plt.title('Product Distribution by Category')

    # Saving the chart to a file
    chart_path = 'C:\\Users\\Dell\\Downloads\\Code Zip1\\Code Zip\\Backend\\Flipkart\\Flipkart\\flipkart\\products\\graphs\\pie_chart.png'
    plt.savefig(chart_path)
    print(categories,category_percentages)
    print("hello")

    # Closing the plot
    plt.close()

    # Sending the chart path along with the data to the template
    data = {
        'category_percentages': category_percentages,
        'chart_path': chart_path,
    }
    return render(request, 'pie_chart.html', data)


def bar_chart_stock_quantities(request):
    products = Products.objects.all()
    product_names = [product.product_name for product in products]
    stock_quantities = [product.stock_quantity for product in products]

    plt.figure(figsize=(10, 5))
    plt.bar(product_names, stock_quantities)
    plt.xlabel('Products')
    plt.ylabel('Stock Quantity')
    plt.title('Stock Quantities of Products')
    plt.xticks(rotation=90)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return HttpResponse(buffer, content_type='image/png')


def pie_chart_product_categories(request):
    categories = ProductsCategory.objects.values_list('category', flat=True).distinct()
    category_counts = [ProductsCategory.objects.filter(category=category).count() for category in categories]

    plt.figure(figsize=(8, 8))
    plt.pie(category_counts, labels=categories, autopct='%1.1f%%')
    plt.title('Product Categories Distribution')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return HttpResponse(buffer, content_type='image/png')


def line_chart_product_prices(request):
    products = Products.objects.all()
    product_names = [product.product_name for product in products]
    prices = [product.price for product in products]

    plt.figure(figsize=(10, 5))
    plt.plot(product_names, prices, marker='o')
    plt.xlabel('Products')
    plt.ylabel('Price')
    plt.title('Product Prices')
    plt.xticks(rotation=90)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return HttpResponse(buffer, content_type='image/png')


def histogram_product_ratings(request):
    ratings = ProductReviewsRatings.objects.values_list('rating', flat=True)

    plt.figure(figsize=(8, 5))
    sns.histplot(ratings, bins=10, kde=True)
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.title('Product Ratings Distribution')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return HttpResponse(buffer, content_type='image/png')


def scatter_plot_price_vs_stock(request):
    products = Products.objects.all()
    prices = [product.price for product in products]
    stock_quantities = [product.stock_quantity for product in products]

    plt.figure(figsize=(10, 5))
    plt.scatter(prices, stock_quantities)
    plt.xlabel('Price')
    plt.ylabel('Stock Quantity')
    plt.title('Price vs Stock Quantity')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return HttpResponse(buffer, content_type='image/png')












