from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Destination, Favorite, UserProfile
from .serializers import DestinationSerializer, FavoriteSerializer, RegisterSerializer, UserSerializer


class DestinationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DestinationSerializer
    queryset = Destination.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.query_params.get("search", "").strip()
        region = self.request.query_params.get("region", "").strip()
        country = self.request.query_params.get("country", "").strip()
        state = self.request.query_params.get("state", "").strip()
        featured = self.request.query_params.get("featured", "").strip().lower()

        if query:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(city__icontains=query) |
                Q(state__icontains=query) |
                Q(country__icontains=query) |
                Q(description__icontains=query)
            )
        if region:
            qs = qs.filter(region__iexact=region)
        if country:
            qs = qs.filter(country__iexact=country)
        if state:
            qs = qs.filter(state__iexact=state)
        if featured in {"1", "true", "yes"}:
            qs = qs.filter(is_featured=True)
        return qs


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "user": UserSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.data.get("full_name") is not None:
        profile.full_name = request.data.get("full_name", "")
        profile.save(update_fields=["full_name"])
    return Response(UserSerializer(request.user).data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def favorites(request):
    if request.method == "GET":
        return Response(FavoriteSerializer(request.user.favorites.select_related("destination"), many=True).data)

    destination_id = request.data.get("destination_id")
    try:
        destination = Destination.objects.get(pk=destination_id)
    except Destination.DoesNotExist:
        return Response({"detail": "Destination not found."}, status=status.HTTP_404_NOT_FOUND)
    favorite, created = Favorite.objects.get_or_create(user=request.user, destination=destination)
    return Response(FavoriteSerializer(favorite).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_favorite(request, destination_id):
    deleted, _ = Favorite.objects.filter(user=request.user, destination_id=destination_id).delete()
    return Response({"deleted": bool(deleted)})
