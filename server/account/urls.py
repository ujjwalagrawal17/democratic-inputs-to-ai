from django.urls import include, path
from rest_framework.routers import SimpleRouter

from account.views import AuthViewSet

router = SimpleRouter()
router.register("auth", AuthViewSet, 'auth')

urlpatterns = [
    path("", include(router.urls)),
]
