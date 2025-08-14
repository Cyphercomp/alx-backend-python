### chats/pagination.py

from rest_framework.pagination import PageNumberPagination

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MessagePagination(PageNumberPagination):
    """
    Custom pagination for messages, limiting results to 20 per page.
    Also includes total count explicitly in the response.
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Override the default response to include the total count using `page.paginator.count`.
        """
        return Response(
            {
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
