from django.urls import path
from . import views

urlpatterns = [
    path("chatbot/", views.home, name="home"),
    path("chatbot/api/", views.chatbot_api, name="chatbot_api"),
]
