from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import home, MenuViewSet, BookingViewSet

router = DefaultRouter()
router.register('menu',MenuViewSet,basename='menu')
router.register('booking/tables',BookingViewSet,basename='booking')
urlpatterns = [
    path('',home,name='restaurant-home'),
    path('api-token-auth/',obtain_auth_token,name='restaurant-api-token-auth'),
    path('',include(router.urls)),
]
