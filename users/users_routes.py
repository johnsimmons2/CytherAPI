from django.urls import path, include
from rest_framework.routers import DefaultRouter
import users.views as user_views

router = DefaultRouter()
router.register('', user_views.user_api.UserViewSet)

urlpatterns = [
    path('users/', include(router.urls)),
    path('auth/login/', user_views.auth.login_view),
    path('auth/logout/', user_views.auth.logout_view),
    path('auth/register/', user_views.auth.register_view),
    path('auth/check/', user_views.auth.auth_check),
]
