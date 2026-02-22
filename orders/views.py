from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal

from .models import Order, OrderItem
from cart.models import Cart
from .serializers import OrderSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return Response({"error": "Cart is empty"}, status=400)

    total_price = Decimal('0.00')

    for item in cart_items:
        total_price += item.product.price * item.quantity

    order = Order.objects.create(
        user=request.user,
        total_price=total_price
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart_items.delete()

    return Response(
        OrderSerializer(order).data,
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
@permission_classes([AllowAny])
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
