from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency("auth.User"),
    ]

    operations = [
        migrations.CreateModel(
            name="Destination",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160)),
                ("city", models.CharField(blank=True, max_length=120)),
                ("state", models.CharField(blank=True, max_length=120)),
                ("country", models.CharField(max_length=120)),
                ("region", models.CharField(choices=[("India", "India"), ("World", "World")], default="World", max_length=20)),
                ("description", models.TextField()),
                ("image_url", models.URLField(max_length=600)),
                ("tags", models.JSONField(blank=True, default=list)),
                ("best_time", models.CharField(blank=True, max_length=120)),
                ("is_featured", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["region", "country", "state", "city", "name"],
                "indexes": [models.Index(fields=["region"], name="travel_dest_region_1e3fd5_idx"), models.Index(fields=["country"], name="travel_dest_country_7bc67e_idx"), models.Index(fields=["state"], name="travel_dest_state_3f2f0e_idx")],
            },
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(blank=True, max_length=160)),
                ("bio", models.TextField(blank=True)),
                ("avatar_url", models.URLField(blank=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to="auth.user")),
            ],
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("destination", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorite_records", to="travel.destination")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorites", to="auth.user")),
            ],
            options={
                "constraints": [models.UniqueConstraint(fields=("user", "destination"), name="unique_user_destination_favorite")],
            },
        ),
    ]
