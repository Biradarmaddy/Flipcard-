import os
import django
from faker import Faker
from django.shortcuts import get_object_or_404

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flipkart.settings")
django.setup()
from products.models import Products,ProductsCategory,ProductImages,TagsKeywords,ProductReviewsRatings,ProductInteraction
from faker import Faker
from django.contrib.auth.models import User

def main():
    name = "C"
    description = "any"
    brand = "Country Delight"
    price = 100
    stock_quantity = 160
    sku = 123424

    prod1 = Products(product_name=name,product_description=description,brand=brand,
                    price=price,stock_quantity=stock_quantity,sku=sku)
    prod1.save()

    prod = Products.objects.filter(sku=sku)[0]

    category = "Dairy"
    subcategory1 = "Farm"
    subcategory2 = "Milk"

    prod_cat = ProductsCategory(category=category,subcategory1=subcategory1,subcategory2=subcategory2)
    prod_cat.product = prod

    tags = "milk"
    key = TagsKeywords(keyword=tags)
    key.product = prod

    review = "Good"
    rating = 4.2
    prod_rating = ProductReviewsRatings(review=review,rating=rating)
    prod_rating.product = prod

    prod_interaction = ProductInteraction()
    user = get_object_or_404(User,pk=1)
    prod_interaction.product = prod
    prod_interaction.user = user


    prod_rating.save()
    prod_cat.save()
    key.save()



if __name__ == "__main__":
    print("Started Populating......")
    main()
    print("Done")