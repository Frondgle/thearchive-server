from django.contrib import admin
from .models import Art, Tag

# Register your models here.

# admin.site.register(Art)
admin.site.register(Tag)


@admin.register(Art)
class ArtAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'style', 'location', 'description', 'color',
                    'frame_type', 'mods', 'date_created', 'film_type', 'malfunction', 'get_tags')

    def get_tags(self, instance):
        return [tag.name for tag in instance.tags.all()]
