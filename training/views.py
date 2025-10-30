from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Exam, ExamResult, Question, Choice
from jobs.models import JobBase, EmployeeJob

# -------------------------------
# Available exams for logged-in user
# -------------------------------
class AvailableExamView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = 'training/available_exams.html'
    context_object_name = 'exams'

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'profile'):
            return Exam.objects.none()

        # Get all jobs tied to this user
        employee_jobs = user.profile.employee_jobs.values_list('job', flat=True)
        return Exam.objects.filter(job__in=employee_jobs).distinct()


# -------------------------------
# Detail view (Exam information)
# -------------------------------
class ExamDetailView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = 'training/exam_detail.html'


# -------------------------------
# Actual exam form / submission
# -------------------------------
class ServerExamView(LoginRequiredMixin, View):
    template_name = "training/server_exam_form.html"

    def get(self, request, pk):
        exam = get_object_or_404(Exam, pk=pk)
        # Prefetch related choices to avoid N+1 queries
        questions = exam.questions.prefetch_related('choices')
        return render(request, self.template_name, {
            'exam': exam,
            'questions': questions,
        })

    def post(self, request, pk):
        exam = get_object_or_404(Exam, pk=pk)
        questions = exam.questions.prefetch_related('choices')

        total = questions.count()
        correct = 0

        for question in questions:
            selected_choice_id = request.POST.get(f"question_{question.id}")
            if not selected_choice_id:
                continue  # skipped question
            try:
                selected_choice = Choice.objects.get(id=selected_choice_id)
                if selected_choice.is_correct:
                    correct += 1
            except Choice.DoesNotExist:
                continue

        percentage = round((correct / total) * 100, 2)
        passed = percentage >= exam.passing_score

        # Save result
        ExamResult.objects.create(
            profile=request.user.profile,
            exam=exam,
            score=percentage,
            passed=passed,
        )

        return render(request, "training/exam_result.html", {
            "exam": exam,
            "score": percentage,
            "passed": passed
        })

class ExamDashboardView(TemplateView):
    template_name = 'training/exam_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Annotate each job with exam counts
        jobs = JobBase.objects.annotate(
            total_exams=Count('exams', distinct=True)
        )

        # Count who has taken exams
        exam_data = []
        for job in jobs:
            exams = job.exams.all()
            for exam in exams:
                total_takers = ExamResult.objects.filter(exam=exam).count()
                passed = ExamResult.objects.filter(exam=exam, passed=True).count()
                exam_data.append({
                    'job': job.title,
                    'exam_title': exam.title,
                    'season': exam.get_season_display(),
                    'year': exam.year,
                    'total_takers': total_takers,
                    'passed': passed,
                })

        context['jobs'] = jobs
        context['exam_data'] = exam_data
        return context

class UserExamDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'training/user_exam_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile

        # Get the user's primary job
        primary_job = (
            EmployeeJob.objects.filter(profile=profile, is_primary=True)
            .select_related("job")
            .first()
        )

        # If no primary job is found, show a message
        if not primary_job:
            context["error"] = "No primary job assigned. Please contact admin."
            return context

        # All exams for this user's job
        exams = Exam.objects.filter(job=primary_job.job)

        # Exams the user has taken
        taken_results = ExamResult.objects.filter(profile=profile)
        taken_exam_ids = taken_results.values_list('exam_id', flat=True)

        # Exams not yet taken
        remaining_exams = exams.exclude(id__in=taken_exam_ids)

        # Stats
        total_exams = exams.count()
        taken_count = taken_results.count()
        passed_count = taken_results.filter(passed=True).count()
        remaining_count = remaining_exams.count()

        context.update({
            'profile': profile,
            'primary_job': primary_job.job,
            'exams': exams,
            'taken_results': taken_results,
            'remaining_exams': remaining_exams,
            'total_exams': total_exams,
            'taken_count': taken_count,
            'passed_count': passed_count,
            'remaining_count': remaining_count,
        })
        return context