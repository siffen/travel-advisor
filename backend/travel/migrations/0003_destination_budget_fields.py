# Generated manually for the Travel Advisor budget planner.
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("travel", "0002_rename_travel_dest_region_1e3fd5_idx_travel_dest_region_025016_idx_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="destination",
            name="daily_budget_low",
            field=models.PositiveIntegerField(default=1500, help_text="Indicative per-person daily spend in INR, excluding long-distance travel."),
        ),
        migrations.AddField(
            model_name="destination",
            name="daily_budget_mid",
            field=models.PositiveIntegerField(default=3000, help_text="Indicative per-person daily spend in INR, excluding long-distance travel."),
        ),
        migrations.AddField(
            model_name="destination",
            name="daily_budget_high",
            field=models.PositiveIntegerField(default=6500, help_text="Indicative per-person daily spend in INR, excluding long-distance travel."),
        ),
        migrations.AddField(
            model_name="destination",
            name="budget_note",
            field=models.CharField(default="Indicative estimate per person/day in INR; excludes flights, trains and other long-distance travel.", max_length=240),
        ),
    ]
