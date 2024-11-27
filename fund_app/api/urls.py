from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FaucetViewSet, APIRoot

# Create a router and register our viewset
router = DefaultRouter(trailing_slash=False)
router.register('faucet', FaucetViewSet, basename='faucet')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', APIRoot.as_view(), name='api-root')
] + router.urls
