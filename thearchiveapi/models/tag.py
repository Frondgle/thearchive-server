from django.db import models


class Tag(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category
