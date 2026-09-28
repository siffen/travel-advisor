from django.contrib.auth.models import User
from django.db import models


class Destination(models.Model):
    REGION_CHOICES = [("India", "India"), ("World", "World")]

    name = models.CharField(max_length=160)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120)
    region = models.CharField(max_length=20, choices=REGION_CHOICES, default="World")
    description = models.TextField()
    image_url = models.URLField(max_length=600)
    tags = models.JSONField(default=list, blank=True)
    best_time = models.CharField(max_length=120, blank=True)
    daily_budget_low = models.PositiveIntegerField(default=1500, help_text="Indicative per-person daily spend in INR, excluding long-distance travel.")
    daily_budget_mid = models.PositiveIntegerField(default=3000, help_text="Indicative per-person daily spend in INR, excluding long-distance travel.")
    daily_budget_high = models.PositiveIntegerField(default=6500, help_text="Indicative per-person daily spend in INR, excluding long-distance travel.")
    budget_note = models.CharField(max_length=240, default="Indicative estimate per person/day in INR; excludes flights, trains and other long-distance travel.")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["region", "country", "state", "city", "name"]
        indexes = [
            models.Index(fields=["region"]),
            models.Index(fields=["country"]),
            models.Index(fields=["state"]),
        ]

    def __str__(self):
        location = ", ".join(part for part in [self.city, self.state, self.country] if part)
        return f"{self.name} — {location}" if location else self.name


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="favorite_records")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "destination"], name="unique_user_destination_favorite")]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=160, blank=True)
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)

    def __str__(self):
        return self.user.username
