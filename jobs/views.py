from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import JobBase, EmployeeJob
from .forms import JobBaseForm, EmployeeJobForm
from django.contrib.auth.mixins import LoginRequiredMixin

class JobBaseListView(LoginRequiredMixin, ListView):
    model = JobBase
    template_name = 'jobs/jobbase_list.html'
    context_object_name = 'jobs'
    ordering = ['title']


class JobBaseCreateView(LoginRequiredMixin, CreateView):
    model = JobBase
    form_class = JobBaseForm
    template_name = 'jobs/jobbase_form.html'
    success_url = reverse_lazy('jobbase_list')


class JobBaseUpdateView(LoginRequiredMixin, UpdateView):
    model = JobBase
    form_class = JobBaseForm
    template_name = 'jobs/jobbase_form.html'
    success_url = reverse_lazy('jobbase_list')


class JobBaseDeleteView(LoginRequiredMixin, DeleteView):
    model = JobBase
    template_name = 'jobs/jobbase_confirm_delete.html'
    success_url = reverse_lazy('jobbase_list')

class EmployeeJobListView(LoginRequiredMixin, ListView):
    model = EmployeeJob
    template_name = 'jobs/employeejob_list.html'
    context_object_name = 'employee_jobs'

class EmployeeJobCreateView(LoginRequiredMixin, CreateView):
    model = EmployeeJob
    form_class = EmployeeJobForm
    template_name = 'jobs/employeejob_form.html'
    success_url = reverse_lazy('employeejob_list')

    def form_valid(self, form):
        # Optional: Automatically assign creator
        form.instance.created_by = self.request.user
        return super().form_valid(form)
