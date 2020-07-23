from django.urls import path,include
from django.conf.urls import url
from django.views.static import serve
from rest_framework.authtoken import views
from django.conf import settings
from rest_framework import routers
from .views import (
    UserViewSet,
    CustomAuthToken,
    MyUserView,
    SignUpView,
    TypeAccountsView,
    DepositoView,
    WithDrawView,
    MyAccountsView
        #AccountsListView,
)


router= routers.DefaultRouter()
router.register('admin/users',UserViewSet)
router.register('admin/type_accounts',TypeAccountsView)
router.register('my_accounts',MyAccountsView)
accounts = [
    path('', include(router.urls)),
    path('my_user/', MyUserView.as_view()),
    #path('my_accounts/', AccountsListView.as_view()),
    path('sign-up/',SignUpView.as_view()),
    path('deposit/',DepositoView.as_view()),
    path('withdraw/', WithDrawView.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', CustomAuthToken.as_view()),
    url(
        regex=r'^media/(?P<path>.*)$',
        view=serve,
        kwargs={'document_root': settings.MEDIA_ROOT}
    ),
]