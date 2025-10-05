from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, blank=True, null=True)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
       return f"{self.name} - {self.sent_at.strftime('%Y-%m-%d')}"
    
    class Meta:
       ordering = ['-sent_at']
       verbose_name = 'Contact Message'
       verbose_name_plural = 'Contact Messages'