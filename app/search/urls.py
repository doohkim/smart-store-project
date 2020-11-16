from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from search.views import SingleKeywordSearchAPIView, \
    MultiKeywordSearchAPIView, TestMultiKeywordSearchAPIView, SingleZeroKeywordSearchAPIView, \
    SingleFirstKeywordSearchAPIView, SingleSecondKeywordSearchAPIView, SingleThirdKeywordSearchAPIView

app_name = 'search'
urlpatterns_v1 = [
    # 제대로 돌아감 키워드 하나 받아서 DRF로 구현함
    path('single_drf/', SingleKeywordSearchAPIView.as_view(), name='single'),
    ############################################################################

    path('test0/', SingleZeroKeywordSearchAPIView.as_view(), name='get1'),
    path('test1/', SingleFirstKeywordSearchAPIView.as_view(), name='get2'),
    path('test2/', SingleSecondKeywordSearchAPIView.as_view(), name='get3'),
    path('test3/', SingleThirdKeywordSearchAPIView.as_view(), name='get4'),
    path('test4/', SingleZeroKeywordSearchAPIView.as_view(), name='get5'),
    path('test5/', SingleFirstKeywordSearchAPIView.as_view(), name='get6'),
    path('test6/', SingleSecondKeywordSearchAPIView.as_view(), name='get7'),
    path('test7/', SingleThirdKeywordSearchAPIView.as_view(), name='get8'),
    path('test8/', SingleZeroKeywordSearchAPIView.as_view(), name='get9'),
    path('test9/', SingleFirstKeywordSearchAPIView.as_view(), name='get10'),

    ##########################################################################
    # 구현예정 api
    # path('download_link/test/', views., name='download'),
    # url(r'^download/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('uploadtest/', TestMultiKeywordSearchAPIView.as_view(), name='get'),

    # 단순 test django 이용해 프로토타입 구현한거
    # path('single/test/', views.naver_api_single_django, name='test'),
    # # 업로드한 엑셀파일에서 키워드 가져와서 여러가지 키워드 api 가져오는 api
    path('upload/test/', MultiKeywordSearchAPIView.as_view(), name='upload'),
    #
    # path('down/test/', views.download_csv_file_api, name='down'),
]

urlpatterns = [
    path('v1/', include(urlpatterns_v1)),
]

urlpatterns = format_suffix_patterns(urlpatterns)
