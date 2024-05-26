from django.core import paginator
from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from base.models import Product, Review
from base.serializers import ProductSerializer


from django.contrib.auth.hashers import make_password
from rest_framework import serializers, status

from base.serializers import OrderSerializer

@api_view(["GET"])
def get_products(request):
    query = request.query_params.get('keyword')

    if query == None:
        query = ""

    products = Product.objects.filter(name__icontains=query)

    page = request.query_params.get('page')
    paginator = Paginator(products, 8)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)

    serializer = ProductSerializer(products, many=True)

    return Response({'products':serializer.data, 'page':page, 'pages':paginator.num_pages})

@api_view(["GET"])
def get_top_products(request):
    products = Product.objects.filter(rating__gte=4).order_by('-rating')[0:5]
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)

@api_view(["GET"])
def get_product(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)

    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_product(request):
    user = request.user

    product = Product.objects.create(
        user=user,
        name="Sample Name",
        price=0.00,
        brand="Sample Brand",
        countInStock=0,
        category="Sample Category",
        description=""
    )

    serializer = ProductSerializer(product, many=False)

    return Response(serializer.data)

@api_view(["PUT"])
@permission_classes([IsAdminUser])
def update_product(request, pk):
    data = request.data
    product = Product.objects.get(_id=pk)

    product.name = data["name"]
    product.price = data["price"]
    product.brand = data["brand"]
    product.countInStock = data["countInStock"]
    product.category = data["category"]
    product.description = data["description"]

    product.save()

    serializer = ProductSerializer(product, many=False)

    return Response(serializer.data)

@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_product(request, pk):
    product = Product.objects.get(_id=pk)
    product.delete()

    return Response('Product deleted')

@api_view(["POST"])
@permission_classes([IsAdminUser])
def upload_image(request):
    data = request.data

    product_id = data["product_id"]
    product = Product.objects.get(_id=product_id)

    # Check for file upload
    product.image = request.FILES.get('image')
    product.save()

    return Response("Image was uploaded")

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_product_review(request, pk):
    user = request.user
    product = Product.objects.get(_id=pk)
    data = request.data
    customer_rating = int(data['rating'])
    customer_orders = user.order_set.all()
    orders = OrderSerializer(customer_orders, many=True).data
    ordered_items = list()
    already_exists = product.review_set.filter(user=user).exists()

    for order in orders:
        for item in order["orderItems"]:
            ordered_items.append(item["product"])
            
    unique_order_items = set(ordered_items)

    if customer_rating == 0:
        content = {'detail':'Need a valid rating please.'}

        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    elif product._id not in unique_order_items:
        content = {'detail':'You can\'t possibly know anything about this item'}

        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    elif already_exists:
        content = {'detail':'Product already reviewed'}

        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    elif customer_rating <= 0 or customer_rating > 5:
        content = {'detail':'You keep a reviewin\', but ya can\'t fool me'}

        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment']
        )

        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating

        product.rating = total / len(reviews)
        product.save()

        return Response('Review added')

@api_view(["POST"])
def reset(request):
    name = request.data["name"]
    
    Review.objects.filter(name=name).delete()
    
    return Response("We reset some thingies!")
