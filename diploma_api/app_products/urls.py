from django.urls import path

from .views import *

urlpatterns = [
    path('<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('<int:pk>/review', ReviewCreatView.as_view(), name='create_review'),
]
