from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

class Reviewlistpagination(PageNumberPagination):
    page_size = 1   # 2,3 4....
    page_query_param = 'pa'
    page_size_query_param = 'size' #value,record
    max_page_size = 1  # 2,3,4...
    last_page_string = 'last'

class Reviewlistlimitoffpag(LimitOffsetPagination):
    default_limit = 3 #2,3,4..
    max_limit = 2
     # to change the name of offset
    offset_query_param = 'start'
    limit_query_param = 'limitsss'


class Reviewlistcursorpag(CursorPagination):
    page_size = 3
    # ordering = 'created'
    ordering = '-rating'  # rating -- 1 to 5 , -rating -- 5 to 1