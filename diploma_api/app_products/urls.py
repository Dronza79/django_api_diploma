from django.urls import path

from .views import *

urlpatterns = [
    path('<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('<int:pk>/review', ReviewCreatView.as_view(), name='create_review'),
    path('limited', ProductLimitedView.as_view(), name='prod_limited'),
    path('popular', ProductPopularView.as_view(), name='prod_limited'),
]
