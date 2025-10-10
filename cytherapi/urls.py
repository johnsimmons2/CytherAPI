"""
URL configuration for cytherapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from cytherapi.views import health_check
from django.contrib.auth.decorators import user_passes_test
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
import users.users_routes as user_routes
import notes.notes_routes as notes_routes

# not pythonic
# is_admin = (lambda u: u.is_staff and u.is_authenticated)

# correct pythonic way apparently
def is_admin(user): return user.is_staff and user.is_authenticated

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(user_routes.urlpatterns)),
    path('api/', include(notes_routes.urlpatterns)),
    
    # Documentation
    path('api/docs/', user_passes_test(is_admin)(SpectacularAPIView.as_view()), name='schema'),
    path('api/docs/swagger/', user_passes_test(is_admin)(SpectacularSwaggerView.as_view(url_name='schema')), name='swagger-ui'),
    
    # Core / Global
    path('api/health', health_check)
]
