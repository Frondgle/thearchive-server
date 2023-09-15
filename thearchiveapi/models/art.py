from django.db import models

class Art(models.Model):
    pic = models.URLField()
    title = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    style = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    color = models.BooleanField(default=True)
    frame_type = models.CharField(max_length=50)
    mods = models.BooleanField(default=False)
    date_created = models.IntegerField()
    film_type = models.CharField(max_length=50)
    malfunction = models.BooleanField(default=False)
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, related_name="art_tag", null=True)
