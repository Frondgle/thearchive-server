from django.contrib import admin
from .models import Art, Tag


class ArtAdmin(admin.ModelAdmin):
    """Class to customize the admin interface for the Art model. 
      Filter_horizontal OR filter_vertical widget/layout
      to add the tags field to the Art model admin page.
  """
    # Other admin options for the Art model
    # ...
    filter_horizontal = ('tags',)
    # filter_vertical = ('tags',)

# Register your models with the custom admin class
admin.site.register(Art)
admin.site.register(Tag)
