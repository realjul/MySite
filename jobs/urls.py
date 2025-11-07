from django.urls import path
from .views import (
    JobBaseListView, JobBaseCreateView, JobBaseUpdateView, JobBaseDeleteView,
    EmployeeJobListView, EmployeeJobCreateView
)

urlpatterns = [
    # JobBase URLs
    path('jobs/', JobBaseListView.as_view(), name='jobbase_list'),
    path('jobs/new/', JobBaseCreateView.as_view(), name='jobbase_create'),
    path('jobs/<int:pk>/edit/', JobBaseUpdateView.as_view(), name='jobbase_update'),
    path('jobs/<int:pk>/delete/', JobBaseDeleteView.as_view(), name='jobbase_delete'),

    # EmployeeJob URLs
    path('employee-jobs/', EmployeeJobListView.as_view(), name='employeejob_list'),
    path('employee-jobs/new/', EmployeeJobCreateView.as_view(), name='employeejob_create'),
]
