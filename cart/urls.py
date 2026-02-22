from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.get_cart),
    path("cart/add/", views.add_to_cart),
    path("cart/remove/", views.remove_from_cart),
]