from rest_framework.pagination import PageNumberPagination


class UsersPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
