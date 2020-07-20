from django.urls import path,include
from django.conf.urls import url
from django.views.static import serve
from rest_framework.authtoken import views
from django.conf import settings
from rest_framework import routers
from .views import (
    UserViewSet,
    CustomAuthToken
)


router= routers.DefaultRouter()
router.register('users',UserViewSet)

accounts = [
    path('', include(router.urls)),
    #path('/my_user/', MyUser.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', CustomAuthToken.as_view()),
    url(
        regex=r'^media/(?P<path>.*)$',
        view=serve,
        kwargs={'document_root': settings.MEDIA_ROOT}
    ),
]