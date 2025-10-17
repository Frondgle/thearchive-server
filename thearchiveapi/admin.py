from django.contrib import admin
from .models import Art, Tag, Subscriber, ContactMessage
from .forms import ArtForm

# Register your models here.

# admin.site.register(Art)
admin.site.register(Tag)


@admin.register(Art)
class ArtAdmin(admin.ModelAdmin):
    form = ArtForm
    list_display = (
        "title",
        "code",
        "style",
        "location",
        "description",
        "color",
        "frame_type",
        "mods",
        "date_created",
        "film_type",
        "malfunction",
        "display_tags",
    )
    list_filter = ("tags",)  # Add this to filter by tags

    def display_tags(self, instance):
        return ", ".join([tag.category for tag in instance.tags.all()])

    display_tags.short_description = "Tags"  # Set the column name in the admin


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "subscribed_at"]
    search_fields = ["email"]
    readonly_fields = ["subscribed_at"]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "sent_at", "short_content")
    list_filter = ("sent_at",)
    search_fields = ("name", "email", "content")
    readonly_fields = ("sent_at",)
    ordering = ("-sent_at",)

    # Shows fields when viewing/editing individual message
    fields = ("name", "email", "content", "sent_at")

    def short_content(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    short_content.short_description = "Message Preview"
