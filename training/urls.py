from django.urls import path
from .views import AvailableExamView, ExamDetailView, ExamView, ExamDashboardView, UserExamDashboardView

urlpatterns = [
    path("available_exams/", AvailableExamView.as_view(), name="available_exams"),
    path("exam/<int:pk>/", ExamDetailView.as_view(), name="exam_detail"),
    path("exam/<int:pk>/take/", ExamView.as_view(), name="server_exam"),
    path("dashboard/", ExamDashboardView.as_view(), name="exam_dashboard"),
    path("user_exam_dashboard/", UserExamDashboardView.as_view(), name="user_exam_dashboard"),
]
