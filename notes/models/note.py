from django.db import models
from users.models.user import User
from notes.models.tag import Tag


class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    directory = models.CharField(max_length=255, blank=True)
    shared_users = models.ManyToManyField(User, through='NoteSharedUser', related_name='shared_notes')

    def __str__(self):
        return f"[{self.pk}] {self.title} | {self.owner}"

class NoteSharedDirectory(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='directory_shares')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_directory_shares')
    share_date = models.DateTimeField(auto_now_add=True)
    directory = models.CharField(max_length=255)
    
    class Meta:
        unique_together = ('owner', 'directory', 'shared_with')
    
class NoteSharedUser(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='user_shares')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_user_shares')
    share_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('note', 'shared_with')

class NoteTag(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='notes')

    class Meta:
        unique_together = ('note', 'tag')