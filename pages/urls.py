from django.urls import path
from .views import HomePageView, AboutPageView

"""You must import HomePageView in your urls.py file, you must create a HomePageView"""
urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
]