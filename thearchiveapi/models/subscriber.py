from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(unique=True, max_length=255)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ['-subscribed_at']