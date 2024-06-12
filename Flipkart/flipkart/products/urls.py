from django.urls import path

from . import views

urlpatterns = [
    path("data/<int:id>",views.getSingleProdct,name="getSingleProduct"),
    path("data/",views.getAll,name="getAll"),
    path("data/<slug:cat>",views.getCategoryProducts,name="getCategoryProducts"),
    path("data/<slug:keyword>",views.search,name="search"),
    path("increment/<int:pid>/<int:uid>",views.getIncrement,name="increment"),
    path("data/top/products",views.top_products,name="top_products"),
    path("data/pie",views.pie_chart,name="category_wise_product"),
    path('bar_chart_stock_quantities/', views.bar_chart_stock_quantities, name='bar_chart_stock_quantities'),
    path('pie_chart_product_categories/', views.pie_chart_product_categories, name='pie_chart_product_categories'),
    path('line_chart_product_prices/', views.line_chart_product_prices, name='line_chart_product_prices'),
    path('histogram_product_ratings/', views.histogram_product_ratings, name='histogram_product_ratings'),
    path('scatter_plot_price_vs_stock/', views.scatter_plot_price_vs_stock, name='scatter_plot_price_vs_stock'),


]
