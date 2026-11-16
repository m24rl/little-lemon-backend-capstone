from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from restaurant.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('restaurant/', include('restaurant.urls')),
    path('api/', include('restaurant.api_urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api-auth/', include('rest_framework.urls')),
    path('restaurant/api-token-auth/', obtain_auth_token, name='api-token-auth'),
]
