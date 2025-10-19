import uuid
from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(unique=True, max_length=255)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribe_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["-subscribed_at"]
