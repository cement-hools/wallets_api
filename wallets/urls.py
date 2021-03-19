from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import CreateUserView

registration_router = DefaultRouter()
registration_router.register('reg', CreateUserView, basename='reg')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(registration_router.urls)),
    path('auth/', include('rest_framework.urls')),

    # path('rest-auth/', include('rest_auth.urls')),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),

    path('api/', include('api.urls')),

]
