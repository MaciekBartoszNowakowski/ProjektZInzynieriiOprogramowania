from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('dj_rest_auth.urls')),
    path('users/', include('users.urls')),
    path('thesis/', include('thesis.urls')),
    path('common/', include('common.urls')),
    path('applications/', include('applications.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]