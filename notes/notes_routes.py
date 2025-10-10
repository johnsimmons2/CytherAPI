from django.urls import path, include
from rest_framework.routers import DefaultRouter
import notes.views as notes_views

router = DefaultRouter()
router.register('', notes_views.notes_api.NoteViewSet)

urlpatterns = [
    path('notes/', include(router.urls)),
]
