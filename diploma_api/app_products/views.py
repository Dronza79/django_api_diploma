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
        request.data['prod'] = self.kwargs.get('pk')
        ser = ReviewSerializer(data=request.data)
        ser.is_valid()
        ser.save()
        qs = Review.objects.filter(prod_id=kwargs.get('pk'))
        lst = ReviewSerializer(qs, many=True)
        return Response(data=lst.data)
