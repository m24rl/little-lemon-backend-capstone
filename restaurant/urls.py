from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home, MenuItemsView, SingleMenuItemView, BookingViewSet

router = DefaultRouter()
router.register('tables',BookingViewSet,basename='booking')
urlpatterns = [
    path('',home,name='restaurant-home'),
    path('menu/',MenuItemsView.as_view(),name='menu-list'),
    path('menu/<int:pk>/',SingleMenuItemView.as_view(),name='menu-detail'),
    path('booking/',include(router.urls)),
]
