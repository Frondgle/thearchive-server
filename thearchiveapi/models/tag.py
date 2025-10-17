from django.db import models
from django.db.models.functions import Lower


class Tag(models.Model):
    category = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("category"), name="unique_lower_category")
        ]

    def __str__(self):
        return self.category
