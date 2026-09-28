from django.contrib import admin
from .models import Destination, Favorite, UserProfile


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "state", "country", "region", "is_featured")
    list_filter = ("region", "country", "state", "is_featured")
    search_fields = ("name", "city", "state", "country")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "destination", "created_at")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name")
