from django.db import models

class Role(models.Model):
    level = models.IntegerField(blank=True, null=True)
    rolename = models.CharField(db_column='roleName', blank=True, null=True)