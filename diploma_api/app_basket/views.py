from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_products.models import Product
from .utils import get_cart, get_data_cart


class BasketView(APIView):

    def get(self, *args, **kwargs):
        response = get_data_cart(self.request)
        return Response(response, status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        data = {
            'product': Product.objects.get(id=self.request.data.get('id')),
            'quantity': self.request.data.get('count')
        }
        print(data)
        get_cart(self.request).add(**data)
        response = get_data_cart(self.request)
        return Response(response, status=status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        prod = Product.objects.get(id=self.request.query_params.get('id'))
        data = {'product': prod}
        if not self.request.query_params.get('count'):
            get_cart(self.request).remove(**data)
        else:
            data['quantity'] = int(self.request.query_params.get('count'))
            data['dec'] = True
            get_cart(self.request).add(**data)
        response = get_data_cart(self.request)
        return Response(response, status=status.HTTP_200_OK)
