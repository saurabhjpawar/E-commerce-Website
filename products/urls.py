from django.urls import path
from .views import category_list, product_list, product_detail

urlpatterns = [
    path('categories/', category_list),
    path('products/', product_list),
    path('products/<int:pk>/', product_detail),
]
