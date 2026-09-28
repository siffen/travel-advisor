from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DestinationViewSet, favorites, me, register, remove_favorite

router = DefaultRouter()
router.register("destinations", DestinationViewSet, basename="destination")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/register/", register),
    path("auth/me/", me),
    path("favorites/", favorites),
    path("favorites/<int:destination_id>/", remove_favorite),
]
