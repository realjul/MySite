from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"

class AboutPageView(TemplateView):
    template_name = "about.html"


@login_required
def profile_page(request):
    return render(request, "profile.html")