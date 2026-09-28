from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("travel", "0001_initial"),
    ]

    operations = [
        migrations.RenameIndex(
            model_name="destination",
            new_name="travel_dest_region_025016_idx",
            old_name="travel_dest_region_1e3fd5_idx",
        ),
        migrations.RenameIndex(
            model_name="destination",
            new_name="travel_dest_country_24d00f_idx",
            old_name="travel_dest_country_7bc67e_idx",
        ),
        migrations.RenameIndex(
            model_name="destination",
            new_name="travel_dest_state_1af5a0_idx",
            old_name="travel_dest_state_3f2f0e_idx",
        ),
    ]
