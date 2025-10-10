from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission, IsAdminUser, AllowAny
from notes.serializers import NoteSerializer
from notes.models.note import Note, NoteSharedDirectory
from notes.models.tag import Tag
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import models


class IsSelfOrAdmin(BasePermission):
    def has_object_permission(self, request: Request, view, obj) -> bool:
        return request.user == obj.owner or request.user.is_staff or request.user.groups.filter(name='Admin').exists()

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    
    def get_permissions(self):
        action_perms = {           
            'list': [IsAdminUser()], # list all notes
            'destroy': [IsAdminUser()], # destroy a note
            'retrieve': [IsSelfOrAdmin()], # get a single note by id
            'update': [IsSelfOrAdmin()],
            'partial_update': [IsSelfOrAdmin()],
        }

        return action_perms.get(self.action, [IsAuthenticated()]) # Eventually, make sure they are also in a campaign



    # def get_queryset(self):
    #     user = self.request.user
    #     return Note.objects.filter(
    #         models.Q(owner=user) |
    #         models.Q(shared_users=user) |
    #         models.Q(directory__in=NoteSharedDirectory.objects.filter(shared_with=user, owner=models.OuterRef('owner')).values('directory')) |
    #         models.Q(tags__in=Tag.objects.filter(models.Q(owner=user) | models.Q(shared_users=user)))
    #     ).distinct()
