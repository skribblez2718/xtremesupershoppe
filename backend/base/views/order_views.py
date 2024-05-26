from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import Product, Order, OrderItem, ShippingAddress
from base.serializers import OrderSerializer

from django.contrib.auth.hashers import make_password
from rest_framework import serializers, status

from datetime import datetime
from decimal import Decimal, getcontext

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_order_items(request):
    user = request.user
    data = request.data
    order_items = data["orderItems"]

    if order_items and len(order_items) == 0:
        return Response({"detail":"No order items"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Check order request to ensure prices match
        tax_amount = Decimal('1.0925')
        pre_tax_price = Decimal('0.0000')
        total_price = Decimal('0.0000')

        for item in order_items:
            product = Product.objects.get(_id=item["product"])

            db_price = (Decimal(product.price).quantize(Decimal('.01')) * Decimal(item["qty"]).quantize(Decimal('.01')))
            pre_tax_price += db_price.quantize(Decimal('.01'))

        shipping_price = Decimal('10.0000')

        if pre_tax_price > Decimal('100.0000'):
            total_price = (pre_tax_price * tax_amount).quantize(Decimal('.01'))
        else:
            total_price = ((pre_tax_price * tax_amount) + shipping_price).quantize(Decimal('.01'))
        print(f"TOTAL_PRICE: {total_price}")
        print(f"DB_PRICE: {Decimal(data['totalPrice']).quantize(Decimal('.01'))}")
        if total_price != Decimal(data["totalPrice"]).quantize(Decimal('.01')):
            return Response({"detail":"Quite fiddlin' with the price"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Create Order
            order = Order.objects.create(
                user=user,
                paymentMethod=data["paymentMethod"],
                taxPrice=data["taxPrice"],
                shippingPrice=data["shippingPrice"],
                totalPrice=data["totalPrice"]
            )
            
            # Create Shipping Address
            shipping = ShippingAddress.objects.create(
                order=order,
                address=data["shippingAddress"]["address"],
                city=data["shippingAddress"]["city"],
                postalCode=data["shippingAddress"]["postalCode"],
                country=data["shippingAddress"]["country"]
            )

            # Create order and set to OrderItem relationship
            for i in order_items:
                product = Product.objects.get(_id=i["product"])
                item = OrderItem.objects.create(
                    product=product,
                    order=order,
                    name=product.name,
                    qty=i["qty"],
                    price=i["price"],
                    image=product.image.url
                )

                # Update product stock
                product.countInStock == item.qty
                product.save()
    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_orders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_order_by_id(request, pk):
    user = request.user

    order = Order.objects.get(_id=pk)

    try:
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)

            return Response(serializer.data)
        else:
            Response({"detail":"Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({"detail":"Order does not exist"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_order_to_paid(request, pk):
    order = Order.objects.get(_id=pk)

    order.isPaid = True
    order.paidAt = datetime.now()
    order.save()

    return Response('Order is paid')

@api_view(["PUT"])
@permission_classes([IsAdminUser])
def update_order_to_delivered(request, pk):
    order = Order.objects.get(_id=pk)

    order.isDelivered = True
    order.deliveredAt = datetime.now()
    order.save()

    return Response('Order was delivered')