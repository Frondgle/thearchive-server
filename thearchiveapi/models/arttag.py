from django.db import models


class ArtTag(models.Model):
    art = models.ForeignKey("Art", on_delete=models.CASCADE)
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)
