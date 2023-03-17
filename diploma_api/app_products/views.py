from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Review
from .serializers import ProductSerializer, ReviewSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ReviewCreatView(APIView):

    def post(self, request, **kwargs):
        print('request.user=', request.user)
        print('request.data=', request.data)
        print('kwargs=', self.kwargs)
        request.data['prod'] = self.kwargs.get('pk')
        if request.user.is_authenticated:
            request.data['author'] = request.user.username
            request.data['email'] = request.user.email
        ser = ReviewSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            qs = Review.objects.filter(prod_id=kwargs.get('pk'))
            lst = ReviewSerializer(qs, many=True)
            return Response(data=lst.data)
        return Response(data=ser.errors)
