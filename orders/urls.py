from django.urls import path
from .views import place_order, order_list

urlpatterns = [
    path('place/', place_order),
    path('', order_list),
]
