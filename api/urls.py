from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', viewset=views.UserViewSet, basename='users')
router.register(r'notes', viewset=views.NoteViewSet, basename='notes')

urlpatterns = router.urls
