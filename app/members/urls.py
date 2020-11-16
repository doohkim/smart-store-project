
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from members import views
from members.views import KIUserCreateAPIView, KIUserActivateAPIView, KIUserLoginAPIView, KIUserLogoutAPIVIew

app_name = 'members'

urlpatterns_v1 = [

    path('signup/', KIUserCreateAPIView.as_view(), name='signup'),
    path('activate/<int:pk>/<str:token>/', KIUserActivateAPIView.as_view(), name='activate'),
    path('login/', KIUserLoginAPIView.as_view(), name='login'),

    # 로그아웃 미정
    path('logout/', KIUserLogoutAPIVIew.as_view(), name='logout'),

    path('rest-auth/', include('rest_auth.urls')),
]

urlpatterns = [
    path('v1/', include(urlpatterns_v1)),
]

urlpatterns = format_suffix_patterns(urlpatterns)
