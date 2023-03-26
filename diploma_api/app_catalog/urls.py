from django.urls import path

from .views import CategoryListView, CatalogListView

urlpatterns = [
    path('categories', CategoryListView.as_view(), name='categories'),
    path('catalog', CatalogListView.as_view(), name='catalog'),
    path('catalog/<int:id>', CatalogListView.as_view(), name='catalog_id'),
]
