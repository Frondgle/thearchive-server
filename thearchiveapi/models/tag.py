from django.db import models

class Tag(models.Model):
  category = models.CharField(max_length=50)
