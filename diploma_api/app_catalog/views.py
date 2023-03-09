from django.shortcuts import render
from rest_framework import generics

from .models import Category
from .serializers import CategorySerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all().prefetch_related('subcategories', 'image')
    serializer_class = CategorySerializer
