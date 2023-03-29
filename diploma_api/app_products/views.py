from django.db.models import Count
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Review, Tag
from .serializers import ProductSerializer, ReviewSerializer, ProductLimitedSerializer, TagsSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ReviewCreatView(APIView):

    def post(self, request, **kwargs):
        # print('request.user=', request.user)
        # print('request.data=', request.data)
        # print('kwargs=', self.kwargs)
        request.data['prod'] = self.kwargs.get('pk')
        if request.user.is_authenticated:
            request.data['author'] = request.user.username
            request.data['email'] = request.user.email
        ser = ReviewSerializer(data=request.data)
        if ser.is_valid():
            # print('ser.validated_data=', ser.validated_data)
            ser.save()
            qs = Review.objects.filter(prod_id=kwargs.get('pk'))
            lst = ReviewSerializer(qs, many=True)
            return Response(data=lst.data)
        # print('ser.errors=', ser.errors)
        return Response(ser.errors, status=400)


class ProductLimitedView(generics.ListAPIView):
    serializer_class = ProductLimitedSerializer

    def get_queryset(self):
        qs = Product.objects.filter(limited=True)
        return qs[:16]


class ProductPopularView(ProductLimitedView):
    def get_queryset(self):
        qs = Product.objects.prefetch_related('reviews').annotate(num_comm=Count('reviews')).exclude(num_comm__lt=3)
        qs = qs.order_by('-num_comm', 'price', '-count')
        return qs[:20]


class TagsView(generics.ListAPIView):
    serializer_class = TagsSerializer
    queryset = Tag.objects.all()

