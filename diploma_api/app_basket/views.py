from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_products.models import Product
from .utils import get_cart


class BasketView(APIView):
    def get(self, request):
        data = [{
            'id': item.product.id,
            'title': item.product.title,
            'price': item.product.price,
            'description': item.product.description,
            'count': item.quantity,
            'href': item.product.href,
            'images': item.product.images,
        } for item in get_cart(request).inside.all()]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        get_cart(request).add(
            product=Product.objects.get(id=request.data.get('id')),
            quantity=request.data.get('count')
        )
        data = [{
            'id': item.product.id,
            'title': item.product.title,
            'price': item.product.price,
            'description': item.product.description,
            'count': item.quantity,
            'href': item.product.href,
            'images': item.product.images,
        } for item in get_cart(request).inside.all()]
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request):
        pass
