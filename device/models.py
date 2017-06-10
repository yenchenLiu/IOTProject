from django.db import models

# Create your models here.


class UserPublicKey(models.Model):
    user = models.OneToOneField('auth.User', related_name='public_key')
    public_key = models.TextField()
