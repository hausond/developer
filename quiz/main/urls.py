from django.urls import path
from .import views

urlpatterns = [
    path('main/', views.ModelsListView.as_view(), name = "model"),
    path('auth/', views.UsersAuthView.as_view(), name = "auth")
]