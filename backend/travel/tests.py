from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from .models import Destination


class TravelAPITest(APITestCase):
    def setUp(self):
        self.destination = Destination.objects.create(
            name="Test City",
            city="Test City",
            state="Test State",
            country="India",
            region="India",
            description="Test destination",
            image_url="https://example.com/test.jpg",
        )

    def test_destination_list(self):
        response = self.client.get("/api/destinations/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["results"][0]["name"], "Test City")

    def test_register_returns_tokens(self):
        response = self.client.post("/api/auth/register/", {
            "username": "traveler",
            "email": "traveler@example.com",
            "password": "StrongPass123!",
            "full_name": "Test Traveler",
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("access", response.data)
        self.assertEqual(User.objects.filter(username="traveler").count(), 1)
