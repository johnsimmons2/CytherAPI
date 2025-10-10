from django.dispatch import receiver
from django.db.models.signals import post_migrate
from notes.models.tag import TagIcons


@receiver(post_migrate)
def create_default_tags(sender, **kwargs):
    from users.models.user import User
    from notes.models.tag import Tag
    
    cyther_user, _ = User.objects.get_or_create(username="cyther.online", defaults={
        'email': 'admin@cyther.online',
        'is_active': False
    })
    
    default_tags = [
        {
            'name': 'General',
            'description': "General notes that don't fit into any other category.",
            'color': 'F94144',
            'icon': TagIcons.FOLDER.value
        },
        {
            'name': 'Character',
            'description': "Notes about specific characters.",
            'color': 'F3722C',
            'icon': TagIcons.PERSON.value
        },
        {
            'name': 'Quest',
            'description': "Quests, side-quests, and plot-hooks.",
            'color': '00ffcc',
            'icon': TagIcons.FLAG.value
        },
                {
            'name': 'Lore',
            'description': "History, lore, and world knowledge.",
            'color': 'F9C74F',
            'icon': TagIcons.BOOK.value
        },
        {
            'name': 'Treasure',
            'description': "Wondrous treasures and artifacts, owned or sought after.",
            'color': '90BE6D',
            'icon': TagIcons.DIAMOND.value
        },
        {
            'name': 'Bestiary',
            'description': "Notes on creatures, beasts, monsters, and enemies.",
            'color': '9933AA',
            'icon': TagIcons.PAW.value
        },
        {
            'name': 'Rumor',
            'description': "Things heard while exploring and eavesdropping.",
            'color': '4D908E',
            'icon': TagIcons.EAR.value
        }
    ]
    
    for tag in default_tags:
        Tag.objects.get_or_create(owner=cyther_user, name=tag['name'], description=tag['description'], color=tag['color'], icon=tag['icon'], is_public=True)
