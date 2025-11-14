from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class ScheduleView(TemplateView):
    template_name = "scheduling/weekly_schedule.html"