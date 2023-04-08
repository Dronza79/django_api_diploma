from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PaginationCatalog(PageNumberPagination):
    page_size = 12

    def get_paginated_response(self, data):
        count = self.page.paginator.count
        last = int(count / self.page_size)
        if last % self.page_size:
            last += 1
        return Response(OrderedDict([
            ('count', count),
            ('currentPage', self.request.query_params.get(self.page_query_param, 1)),
            ('lastPage', last),
            ('items', data)
        ]))


