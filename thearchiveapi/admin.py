from django.contrib import admin
from .models import Art, Tag


class ArtAdmin(admin.ModelAdmin):
    """Class to customize the admin interface for the Art model. 
      Filter_horizontal OR filter_vertical widget/layout
      to add the tags field to the Art model admin page.
  """
    filter_horizontal = ('tags',)
    # filter_vertical = ('tags',)

    # list_display = ('title',
    #                 'code', 'style', 'location', 'description',
    #                 'color', 'frame_type', 'mods', 'date_created',
    #                 'film_type', 'malfunction', 'get_tags')

    # def get_tags(self, obj):
    #     """Method to return a comma-separated list of tags for each art object.
    #     """
    #     return ', '.join([tag.name for tag in obj.tags.all()])

# Register your models with the custom admin class
admin.site.register(Art, ArtAdmin)
admin.site.register(Tag)
