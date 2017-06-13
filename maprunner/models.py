from django.db import models

# Create your models here.


class MapSite(models.Model):
    user = models.ForeignKey('auth.User', related_name='map_site')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    site_class = models.CharField(max_length=31)
    latitude = models.FloatField()
    longitude = models.FloatField()
    range = models.IntegerField()

