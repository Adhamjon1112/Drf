from django.urls import path

from . import views


urlpatterns = [
    path('notes/', views.notes),                        # localhost:8000/api/notes/
    path('notes/<uuid:id>/', views.note),               # localhost:8000/api/notes/edit/:id

    path('users/', views.users),                        # localhost:8000/api/users/
    path('users/<int:id>/', views.user),                # localhost:8000/api/users/1
]