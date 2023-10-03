from django.contrib import admin
from .models import Art, Tag
from .forms import ArtForm

# Register your models here.

# admin.site.register(Art)
admin.site.register(Tag)


@admin.register(Art)
class ArtAdmin(admin.ModelAdmin):
    form = ArtForm
    list_display = ('title', 'code', 'style', 'location', 'description', 'color',
                    'frame_type', 'mods', 'date_created', 'film_type', 'malfunction', 'display_tags')
    list_filter = ('tags',)  # Add this to filter by tags

    def display_tags(self, instance):
        return ", ".join([tag.category for tag in instance.tags.all()])
    display_tags.short_description = 'Tags'  # Set the column name in the admin
