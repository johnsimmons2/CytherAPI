from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    Group.objects.get_or_create(name='Admin')
    Group.objects.get_or_create(name='DungeonMaster')
    Group.objects.get_or_create(name='Player')
    Group.objects.get_or_create(name='Guest')