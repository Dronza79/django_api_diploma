from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ReviewCreatView(APIView):

    def post(self, request, **kwargs):
        print('kwargs=', self.kwargs)
        print('request=', request.data)
        return Response(status=201)

