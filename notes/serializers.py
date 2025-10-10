from rest_framework import serializers
from notes.models.note import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ['created', 'updated']