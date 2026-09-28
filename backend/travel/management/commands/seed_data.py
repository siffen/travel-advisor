from django.core.management.base import BaseCommand
from travel.models import Destination
from travel.image_sources import resolve_image

IMG = {
    "india": "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=1200&q=82",
    "himalaya": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=82",
    "beach": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=82",
    "palace": "https://images.unsplash.com/photo-1477587458883-47145ed94245?auto=format&fit=crop&w=1200&q=82",
    "city": "https://images.unsplash.com/photo-1494522358652-f30e61a60313?auto=format&fit=crop&w=1200&q=82",
    "desert": "https://images.unsplash.com/photo-1470214304380-aadaedcfff1b?auto=format&fit=crop&w=1200&q=82",
    "temple": "https://images.unsplash.com/photo-1514222134-b57cbb8ce073?auto=format&fit=crop&w=1200&q=82",
    "forest": "https://images.unsplash.com/photo-1473448912268-2022ce9509d8?auto=format&fit=crop&w=1200&q=82",
    "africa": "https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?auto=format&fit=crop&w=1200&q=82",
    "europe": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1200&q=82",
    "london": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=1200&q=82",
    "newyork": "https://images.unsplash.com/photo-1485871981521-5b1fd3805eee?auto=format&fit=crop&w=1200&q=82",
    "dubai": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1200&q=82",
    "japan": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=1200&q=82",
    "sydney": "https://images.unsplash.com/photo-1506973035872-a4f4b3d6e7b7?auto=format&fit=crop&w=1200&q=82",
    "bali": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1200&q=82",
    "singapore": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=1200&q=82",
    "newzealand": "https://images.unsplash.com/photo-1469521669194-babb45599def?auto=format&fit=crop&w=1200&q=82",
    "greece": "https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=1200&q=82",
    "italy": "https://images.unsplash.com/photo-1529260830199-42c24126f198?auto=format&fit=crop&w=1200&q=82",
    "thailand": "https://images.unsplash.com/photo-1504214208698-ea1916a2195a?auto=format&fit=crop&w=1200&q=82",
    "turkey": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=1200&q=82",
    "usa": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&w=1200&q=82",
}

INDIA_STATES = {
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Tirupati", "Guntur"],
    "Arunachal Pradesh": ["Itanagar", "Tawang", "Bomdila", "Ziro"],
    "Assam": ["Guwahati", "Dibrugarh", "Jorhat", "Tezpur"],
    "Bihar": ["Patna", "Gaya", "Nalanda", "Muzaffarpur"],
    "Chhattisgarh": ["Raipur", "Bilaspur", "Durg", "Jagdalpur"],
    "Goa": ["Panaji", "Vasco da Gama", "Margao", "Mapusa"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhuj"],
    "Haryana": ["Gurugram", "Faridabad", "Panipat", "Hisar", "Kurukshetra"],
    "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala", "Kullu", "Dalhousie"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Deoghar"],
    "Karnataka": ["Bengaluru", "Mysuru", "Mangaluru", "Hubballi", "Hampi"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Alappuzha", "Munnar"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Gwalior", "Jabalpur", "Ujjain", "Khajuraho"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad", "Kolhapur"],
    "Manipur": ["Imphal", "Ukhrul", "Churachandpur"],
    "Meghalaya": ["Shillong", "Cherrapunji", "Tura"],
    "Mizoram": ["Aizawl", "Lunglei", "Champhai"],
    "Nagaland": ["Kohima", "Dimapur", "Mokokchung"],
    "Odisha": ["Bhubaneswar", "Puri", "Cuttack", "Konark", "Rourkela"],
    "Punjab": ["Amritsar", "Ludhiana", "Jalandhar", "Patiala", "Bathinda"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Jaisalmer", "Ajmer", "Pushkar"],
    "Sikkim": ["Gangtok", "Pelling", "Namchi", "Ravangla"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Ooty", "Kanyakumari", "Thanjavur"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar"],
    "Tripura": ["Agartala", "Udaipur", "Dharmanagar"],
    "Uttar Pradesh": ["Lucknow", "Agra", "Varanasi", "Prayagraj", "Ayodhya", "Mathura"],
    "Uttarakhand": ["Dehradun", "Mussoorie", "Rishikesh", "Nainital", "Haridwar", "Kedarnath"],
    "West Bengal": ["Kolkata", "Darjeeling", "Siliguri", "Digha", "Kalimpong"],
    "Andaman and Nicobar Islands": ["Port Blair", "Havelock Island", "Neil Island"],
    "Chandigarh": ["Chandigarh"],
    "Dadra and Nagar Haveli and Daman and Diu": ["Daman", "Diu", "Silvassa"],
    "Delhi": ["New Delhi", "Delhi"],
    "Jammu and Kashmir": ["Srinagar", "Jammu", "Gulmarg", "Pahalgam"],
    "Ladakh": ["Leh", "Nubra Valley", "Kargil", "Pangong Lake"],
    "Lakshadweep": ["Kavaratti", "Agatti", "Bangaram"],
    "Puducherry": ["Puducherry", "Auroville"],
}

STATE_THEME = {
    "Goa": "beach", "Kerala": "beach", "Andaman and Nicobar Islands": "beach", "Lakshadweep": "beach",
    "Himachal Pradesh": "himalaya", "Uttarakhand": "himalaya", "Sikkim": "himalaya", "Arunachal Pradesh": "himalaya", "Ladakh": "himalaya", "Jammu and Kashmir": "himalaya",
    "Rajasthan": "desert", "Gujarat": "desert", "Madhya Pradesh": "temple", "Uttar Pradesh": "temple", "Odisha": "temple", "Tamil Nadu": "temple",
    "Punjab": "palace", "Haryana": "city", "Maharashtra": "city", "Karnataka": "city", "Telangana": "city", "West Bengal": "city", "Delhi": "city", "Chandigarh": "city",
    "Meghalaya": "forest", "Nagaland": "forest", "Mizoram": "forest", "Manipur": "forest", "Assam": "forest", "Tripura": "forest", "Jharkhand": "forest", "Chhattisgarh": "forest",
}

WORLD = [
    ("Paris", "Paris", "France", "Europe", "The Eiffel Tower, art-filled museums, elegant boulevards and riverfront evenings make Paris a classic city break.", "europe", "Jun–Aug", ["art", "food", "romance"]),
    ("London", "London", "United Kingdom", "World", "A deep mix of royal landmarks, historic neighbourhoods, theatre, museums and modern food culture.", "london", "May–Sep", ["history", "museums", "city"]),
    ("New York City", "New York", "United States", "World", "Skyscrapers, neighbourhood food, Broadway, Central Park and iconic waterfront views packed into one city.", "newyork", "Apr–Jun", ["city", "food", "shopping"]),
    ("Dubai", "Dubai", "United Arab Emirates", "World", "Ultra-modern architecture, desert experiences, beaches and world-class shopping create a high-energy escape.", "dubai", "Nov–Mar", ["luxury", "desert", "shopping"]),
    ("Tokyo", "Tokyo", "Japan", "World", "A fast-moving blend of traditional temples, design, street food, neighbourhood culture and technology.", "japan", "Mar–May", ["food", "culture", "city"]),
    ("Sydney", "Sydney", "Australia", "World", "Harbour views, beaches, coastal walks and a lively restaurant scene make Sydney ideal for city-and-nature travel.", "sydney", "Sep–Nov", ["beach", "nature", "city"]),
    ("Bali", "Bali", "Indonesia", "World", "Tropical beaches, rice terraces, temples and wellness retreats spread across a scenic island.", "bali", "Apr–Oct", ["beach", "wellness", "culture"]),
    ("Singapore", "Singapore", "Singapore", "World", "A clean, compact city known for futuristic architecture, hawker food, gardens and waterfront attractions.", "singapore", "Feb–Apr", ["food", "city", "family"]),
    ("Queenstown", "Queenstown", "New Zealand", "World", "Mountain scenery, alpine lakes and adventure sports make Queenstown a natural playground.", "newzealand", "Dec–Feb", ["adventure", "mountains", "nature"]),
    ("Santorini", "Santorini", "Greece", "World", "Cliffside villages, volcanic landscapes, blue-domed churches and sunset views over the Aegean Sea.", "greece", "Apr–Jun", ["islands", "romance", "views"]),
    ("Rome", "Rome", "Italy", "World", "Ancient ruins, Renaissance art, neighbourhood trattorias and the Vatican create layers of history around every corner.", "italy", "Apr–Jun", ["history", "food", "art"]),
    ("Bangkok", "Bangkok", "Thailand", "World", "Golden temples, vibrant markets, river life and street food create an energetic Southeast Asian city break.", "thailand", "Nov–Feb", ["food", "culture", "city"]),
    ("Istanbul", "Istanbul", "Türkiye", "World", "A cross-continental city of mosques, bazaars, Bosphorus views and layered Byzantine and Ottoman history.", "turkey", "Apr–May", ["history", "food", "markets"]),
    ("Cape Town", "Cape Town", "South Africa", "World", "Ocean, mountains, vineyards and dramatic coastal drives give Cape Town a strong mix of city and outdoors.", "africa", "Nov–Mar", ["nature", "wine", "adventure"]),
    ("Cairo", "Cairo", "Egypt", "World", "A gateway to the pyramids and ancient history, with the Nile, museums and a lively contemporary city around them.", "africa", "Oct–Apr", ["history", "culture", "desert"]),
    ("Maldives", "Maldives", "Maldives", "World", "White-sand islands, clear lagoons and coral reefs make the Maldives a favourite for slow beach travel.", "beach", "Nov–Apr", ["beach", "diving", "relax"]),
    ("Barcelona", "Barcelona", "Spain", "World", "Gaudí architecture, Mediterranean beaches, food markets and walkable neighbourhoods create a varied city break.", "europe", "May–Jun", ["art", "beach", "food"]),
    ("Amsterdam", "Amsterdam", "Netherlands", "World", "Canals, cycling routes, art museums and compact neighbourhoods are easy to explore in a few days.", "europe", "Apr–Jun", ["canals", "art", "cycling"]),
    ("Prague", "Prague", "Czech Republic", "World", "A preserved historic centre with castles, bridges, old-town streets and a strong café culture.", "europe", "Apr–Jun", ["history", "architecture", "cafes"]),
    ("Vancouver", "Vancouver", "Canada", "World", "Mountains meet the Pacific in a city known for parks, waterfront walks and outdoor adventures.", "newzealand", "Jun–Sep", ["nature", "city", "outdoors"]),
    ("Rio de Janeiro", "Rio de Janeiro", "Brazil", "World", "Iconic beaches, granite peaks, samba culture and panoramic city views create a memorable tropical metropolis.", "beach", "Dec–Mar", ["beach", "culture", "views"]),
    ("Machu Picchu", "Cusco Region", "Peru", "World", "An extraordinary Inca citadel set among high Andes peaks and cloud-forest landscapes.", "newzealand", "May–Sep", ["history", "hiking", "mountains"]),
    ("Reykjavik", "Reykjavik", "Iceland", "World", "A small, design-forward capital that opens the door to waterfalls, geothermal landscapes and northern lights.", "europe", "Sep–Mar", ["nature", "roadtrip", "aurora"]),
    ("Swiss Alps", "Interlaken", "Switzerland", "World", "A dramatic mountain region of lakes, cable cars, hiking paths, scenic trains and alpine villages.", "europe", "Jun–Sep", ["mountains", "hiking", "scenery"]),
    ("Petra", "Wadi Musa", "Jordan", "World", "The ancient rock-cut city of Petra combines archaeology, desert landscapes and memorable canyon walks.", "desert", "Mar–May", ["history", "desert", "hiking"]),
    ("Serengeti", "Arusha", "Tanzania", "World", "A vast safari landscape famous for wildlife viewing and dramatic seasonal migrations.", "africa", "Jun–Oct", ["wildlife", "safari", "nature"]),
]


INDIA_BUDGET_BY_THEME = {
    "beach": (1800, 3500, 7000),
    "himalaya": (1800, 3300, 6500),
    "palace": (1600, 3000, 6000),
    "desert": (1700, 3200, 6500),
    "temple": (1500, 2800, 5500),
    "city": (2000, 3800, 7500),
    "forest": (1500, 2800, 5600),
    "india": (1500, 2800, 5500),
}

INDIA_CITY_PREMIUMS = {
    "Mumbai": (2600, 5000, 10000),
    "Delhi": (2400, 4600, 9000),
    "New Delhi": (2400, 4600, 9000),
    "Bengaluru": (2300, 4300, 8500),
    "Hyderabad": (2100, 3900, 7600),
    "Pune": (2100, 3900, 7600),
    "Kolkata": (1900, 3500, 7000),
    "Chennai": (2100, 4000, 7800),
    "Goa": (2500, 4800, 9500),
    "Panaji": (2500, 4800, 9500),
    "Vasco da Gama": (2200, 4100, 8200),
    "Margao": (2000, 3700, 7400),
    "Manali": (2200, 4200, 8500),
    "Leh": (2300, 4300, 9000),
    "Srinagar": (2200, 4200, 8500),
}

WORLD_BUDGETS = {
    "Paris": (5000, 9000, 18000), "London": (6000, 11000, 22000), "New York City": (6500, 12000, 24000),
    "Dubai": (5000, 10000, 22000), "Tokyo": (4500, 8500, 17000), "Sydney": (5500, 10000, 22000),
    "Bali": (2500, 5000, 10000), "Singapore": (4500, 8500, 18000), "Queenstown": (5000, 9000, 18000),
    "Santorini": (5500, 10000, 22000), "Rome": (4500, 8000, 16000), "Bangkok": (2200, 4200, 8500),
    "Istanbul": (2500, 5000, 10000), "Cape Town": (3000, 5500, 11000), "Cairo": (2000, 3800, 8000),
    "Maldives": (7000, 14000, 30000), "Barcelona": (4500, 8500, 17000), "Amsterdam": (5000, 9000, 18000),
    "Prague": (3000, 5500, 11000), "Vancouver": (5500, 10000, 22000), "Rio de Janeiro": (3500, 7000, 14000),
    "Machu Picchu": (3500, 6500, 13000), "Reykjavik": (6000, 11000, 24000), "Swiss Alps": (6500, 12000, 25000),
    "Petra": (3500, 6500, 13000), "Serengeti": (6500, 12000, 25000),
}

def india_budget(state, city):
    if city in INDIA_CITY_PREMIUMS:
        return INDIA_CITY_PREMIUMS[city]
    return INDIA_BUDGET_BY_THEME.get(STATE_THEME.get(state, "india"), INDIA_BUDGET_BY_THEME["india"])

def world_budget(name):
    return WORLD_BUDGETS.get(name, (3500, 6500, 13000))

CITY_DESCRIPTIONS = {
    "Hampi": "Stone temples, boulder-strewn landscapes and the ruins of the Vijayanagara Empire make Hampi a standout heritage escape.",
    "Varanasi": "A spiritual riverfront city known for ghats, boat rides, temples and a deeply distinctive evening atmosphere.",
    "Agra": "Home to the Taj Mahal and Agra Fort, Agra is one of India's best-known heritage destinations.",
    "Jaipur": "The Pink City combines grand forts, palaces, colourful bazaars and Rajasthan's food and craft traditions.",
    "Udaipur": "Lakes, palace architecture and Aravalli hills give Udaipur a slower, scenic feel.",
    "Jaisalmer": "Golden sandstone architecture and desert experiences make Jaisalmer a gateway to the Thar Desert.",
    "Goa": "India's famous coastal escape mixes beaches, Portuguese-era neighbourhoods, seafood and a relaxed pace.",
    "Munnar": "Tea estates, misty hills and cool weather make Munnar a popular mountain retreat in Kerala.",
    "Rishikesh": "A Himalayan foothill town known for the Ganges, yoga, rafting and outdoor adventures.",
    "Manali": "A mountain base for river valleys, snow-season trips, hiking and road journeys through the Himalayas.",
    "Darjeeling": "Tea gardens, mountain views and the heritage Himalayan railway shape Darjeeling's character.",
    "Kochi": "A coastal Kerala city mixing historic trading quarters, art spaces, cafés and backwater access.",
    "Mumbai": "India's financial capital pairs a busy waterfront skyline with heritage architecture, food and entertainment.",
    "Delhi": "A dense capital region where Mughal landmarks, modern government districts, markets and museums sit side by side.",
    "New Delhi": "The capital's planned avenues, monuments, museums and food scene make it a major starting point for India travel.",
    "Bengaluru": "A technology hub with leafy neighbourhoods, cafés, contemporary culture and nearby day trips.",
    "Hyderabad": "Historic monuments, biryani, bazaars and a fast-growing modern city make Hyderabad an easy city break.",
    "Kolkata": "A cultural capital known for literature, colonial-era architecture, food and lively neighbourhoods.",
    "Chennai": "A major South Indian city with beaches, temples, heritage neighbourhoods and a strong classical arts tradition.",
    "Puri": "A temple-and-beach destination famous for the Jagannath Temple and Odisha's coastal culture.",
    "Bhubaneswar": "A temple city with historic architecture and convenient access to Puri and Konark.",
    "Leh": "A high-altitude Himalayan town surrounded by monasteries, mountain passes and stark desert-like landscapes.",
    "Srinagar": "Lakes, houseboats, gardens and Himalayan scenery make Srinagar a major gateway to Kashmir.",
    "Gangtok": "A compact Himalayan capital with monasteries, viewpoints and easy access to Sikkim's mountain landscapes.",
    "Shillong": "A green hill city with waterfalls, viewpoints, cafés and access to Meghalaya's dramatic landscapes.",
    "Panaji": "Goa's capital offers colourful Portuguese-era architecture, riverside walks and easy access to nearby beaches.",
    "Khajuraho": "The UNESCO-listed temple complex is known for intricate medieval stone carvings and architecture.",
}

class Command(BaseCommand):
    help = "Seed Travel Advisor with Indian state/UT cities and world destinations."

    def handle(self, *args, **options):
        Destination.objects.all().delete()
        rows = []
        state_items = list(INDIA_STATES.items())
        featured_states = {"Madhya Pradesh", "Rajasthan", "Goa", "Kerala", "Uttar Pradesh", "Maharashtra", "Himachal Pradesh", "Uttarakhand", "Karnataka", "Sikkim", "Jammu and Kashmir", "Ladakh"}
        for state, cities in state_items:
            theme = STATE_THEME.get(state, "india")
            for city in cities:
                description = CITY_DESCRIPTIONS.get(city, f"Explore {city}, a travel base in {state} with local food, landmarks, neighbourhoods and nearby experiences.")
                rows.append(Destination(
                    name=city,
                    city=city,
                    state=state,
                    country="India",
                    region="India",
                    description=description,
                    image_url=resolve_image(city, city, state, "India", IMG.get(theme, IMG["india"])),
                    tags=["India", state, "city break"],
                    best_time="Oct–Mar",
                    daily_budget_low=india_budget(state, city)[0],
                    daily_budget_mid=india_budget(state, city)[1],
                    daily_budget_high=india_budget(state, city)[2],
                    is_featured=state in featured_states or city in {"Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Kolkata", "Chennai"},
                ))
        for name, city, country, region, description, image_key, best_time, tags in WORLD:
            rows.append(Destination(
                name=name,
                city=city,
                country=country,
                region=region if region in {"India", "World"} else "World",
                description=description,
                image_url=resolve_image(name, city, "", country, IMG.get(image_key, IMG["city"])),
                tags=tags,
                best_time=best_time,
                daily_budget_low=world_budget(name)[0],
                daily_budget_mid=world_budget(name)[1],
                daily_budget_high=world_budget(name)[2],
                is_featured=True,
            ))
        Destination.objects.bulk_create(rows)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(rows)} destinations."))
