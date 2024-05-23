from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, NoteViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'notes', NoteViewSet, basename='note')

urlpatterns = router.urls
