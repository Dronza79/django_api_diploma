from statistics import mean

from django.db.models import Count
from rest_framework import generics

from app_products.models import Product
from app_products.serializers import ProductLimitedSerializer
from .filtres import sort_filter
from .models import Category
from .paginations import PaginationCatalog
from .serializers import CategorySerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all().prefetch_related('subcategories', 'image')
    serializer_class = CategorySerializer


class CatalogListView(generics.ListAPIView):
    serializer_class = ProductLimitedSerializer
    pagination_class = PaginationCatalog

    def get_queryset(self, **kwargs):
        qs = (
            Product.objects.select_related('category')
            .prefetch_related('pictures', 'specifications', 'reviews')
            .alias(rating=Count('reviews__rate'))
            .alias(rev=Count('reviews'))
        )
        filter_queryset = sort_filter(self.request, qs, **self.kwargs)
        return filter_queryset
