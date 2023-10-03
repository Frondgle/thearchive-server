from django.contrib import admin
# Register your models here.
from .models import Art
from .models import Tag

admin.site.register(Art)
admin.site.register(Tag)
