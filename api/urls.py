from django.urls import path

from . import views

urlpatterns = [
    path('notes/', views.get_notes),
    path('users/', views.get_users),
    path('notes/new/', views.create_note),
    path('users/new/', views.create_user),

]