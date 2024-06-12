from django.urls import path
from . import views
urlpatterns = [
    path("data/<int:pk>",views.recommendProducts,name="recommend")
]