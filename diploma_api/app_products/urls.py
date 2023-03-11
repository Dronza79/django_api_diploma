from django.urls import path

from .views import *

urlpatterns = [
    path('<int:pk>', ProductDetailView.as_view(), name='product_detail'),
]
