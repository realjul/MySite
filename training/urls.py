from django.urls import path
from .views import AvailableExamView, ExamDetailView, ServerExamView

urlpatterns = [
    path("available_exams/", AvailableExamView.as_view(), name="available_exams"),
    path("exam/<int:pk>/", ExamDetailView.as_view(), name="exam_detail"),  # ✅ Add this
    path("exam/<int:pk>/take/", ServerExamView.as_view(), name="server_exam"),
]
