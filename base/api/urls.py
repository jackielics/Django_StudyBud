from django.urls import path
from . import views

urlpatterns = [
    path('',  views.getRoutes),
    path('rooms/', views.getRooms), # All Rooms
    path('rooms/<str:pk>/', views.getRoom), # Specific Room
]
