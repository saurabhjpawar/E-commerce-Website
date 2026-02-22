from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem, Product
from .serializers import CartSerializer

@api_view(["GET"])
def get_cart(request):
    cart_id = request.GET.get("cart_id")

    if cart_id:
        cart, created = Cart.objects.get_or_create(id=cart_id)
    else:
        cart = Cart.objects.create()

    serializer = CartSerializer(cart)
    return Response(serializer.data)

@api_view(["POST"])
def add_to_cart(request):
    cart_id = request.data.get("cart_id")
    product_id = request.data.get("product_id")

    cart = Cart.objects.get(id=cart_id)
    product = Product.objects.get(id=product_id)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    return Response({"message": "Added to cart"})

@api_view(["POST"])
def remove_from_cart(request):
    item_id = request.data.get("item_id")

    CartItem.objects.filter(id=item_id).delete()

    return Response({"message": "Item removed"})
