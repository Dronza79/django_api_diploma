from django.urls import path

from app_products.views import TagsView
from .views import *

urlpatterns = [
    path('categories', CategoryListView.as_view(), name='categories'),
    path('catalog', CatalogListView.as_view(), name='catalog'),
    path('catalog/<int:id>', CatalogListView.as_view(), name='catalog_id'),
    path('tags', TagsView.as_view(), name='tags'),
]
