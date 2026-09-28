from django.core.management.base import BaseCommand

from travel.image_sources import resolve_image_with_source
from travel.models import Destination
from travel.management.commands.seed_data import IMG, STATE_THEME, WORLD, INDIA_STATES, india_budget, world_budget


class Command(BaseCommand):
    help = "Refresh destination images from Wikipedia/Wikimedia, keeping existing destination rows."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Ignore the local image cache and fetch fresh images.")

    def handle(self, *args, **options):
        destinations = list(Destination.objects.all())
        updated = 0
        fallbacks = 0
        for index, destination in enumerate(destinations, start=1):
            theme = STATE_THEME.get(destination.state, "india") if destination.country == "India" else None
            fallback = IMG.get(theme, IMG["india"]) if destination.country == "India" else IMG.get("city", IMG["india"])
            image, source_page = resolve_image_with_source(
                destination.name, destination.city, destination.state, destination.country, fallback, refresh=options["force"]
            )
            if image != destination.image_url:
                destination.image_url = image
                destination.save(update_fields=["image_url"])
            updated += 1
            if source_page is None and image == fallback:
                fallbacks += 1
            self.stdout.write(f"[{index}/{len(destinations)}] {destination.name} -> {'Wikimedia' if image != fallback else 'fallback'}")
        self.stdout.write(self.style.SUCCESS(f"Updated {updated} destination images. Fallback images used: {fallbacks}."))
