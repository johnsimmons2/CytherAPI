from enum import Enum
from django.db import models
from django.forms import ValidationError
from users.models.user import User


class Tag(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=32, blank=True)
    icon = models.CharField(max_length=32, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False)
    shared_users = models.ManyToManyField(User, through='TagSharedUser', related_name='shared_tags')
    
    class Meta:
        unique_together = ('owner', 'name')
        
class TagSharedUser(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tag_share')
    share_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tag_share_owner')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tag_share_with')
    share_date = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        super().clean()
        if self.share_owner_id == self.shared_with_id:
            raise ValidationError("You can't share a tag with yourself.")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tag', 'share_owner', 'shared_with'],
                name='unique_share_per_tag_to_user'
            ),
            models.CheckConstraint(
                check=~models.Q(share_owner=models.F('shared_with')),
                name='prevent_self_share'
            )
        ]

class TagIcons(Enum):
    FLAG = 'flagOutline'
    BOOK = 'bookOutline'
    DIAMOND = 'diamondOutline'
    KEY = 'keyOutline'
    PAW = 'pawOutline'
    THUMBSDOWN = 'thumbsDownOutline'
    GIFT = 'giftOutline'
    EAR = 'earOutline'
    HEART = 'heartOutline'
    COLORFILTER = 'colorFilterOutline'
    DICE = 'diceOutline'
    FISH = 'fishOutline'
    EARTH = 'earthOutline'
    FLASK = 'flaskOutline'
    RIBBON = 'ribbonOutline'
    SKULL = 'skullOutline'
    CHECKMARK = 'checkmarkDoneOutline'
    COG = 'cogOutline'
    SEARCH = 'searchOutline'
    STAR = 'starOutline'
    FOLDER = 'folderOutline'
    PERSON = 'personOutline'
    READER = 'readerOutline'