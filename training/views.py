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
        profile = getattr(user, 'profile', None)
        if not profile:
            return Exam.objects.none()

        # Get all jobs tied to this user
        job_ids = profile.employee_jobs.values_list('job_id', flat=True)

        # All exams for those jobs
        exams = Exam.objects.filter(job_id__in=job_ids).distinct()

        # Identify passed exams (to exclude them)
        passed_exam_ids = ExamResult.objects.filter(
            profile=profile, passed=True
        ).values_list('exam_id', flat=True)

        # Exams not yet passed (either failed or not taken)
        available_exams = exams.exclude(id__in=passed_exam_ids)

        # Get user's latest attempt for each exam
        results = (
            ExamResult.objects.filter(profile=profile)
            .order_by('exam_id', '-submitted_at')
        )
        result_dict = {}
        for r in results:
            result_dict.setdefault(r.exam_id, r)  # keep only the latest result per exam

        for exam in available_exams:
            result = result_dict.get(exam.id)
            if result:
                exam.has_taken = True
                exam.passed = result.passed
                exam.score = result.score
                exam.last_attempt = result.submitted_at
                exam.can_retake = not result.passed
            else:
                exam.has_taken = False
                exam.passed = None
                exam.score = None
                exam.last_attempt = None
                exam.can_retake = True

        return available_exams

# -------------------------------
# Detail view (Exam information)
# -------------------------------
class ExamDetailView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = 'training/exam_detail.html'


# -------------------------------
# Actual exam form / submission
# -------------------------------
class ExamView(LoginRequiredMixin, View):
    template_name = "training/exam_form.html"

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

        # Get user's primary job (if exists)
        primary_job = (
            EmployeeJob.objects.filter(profile=profile, is_primary=True)
            .select_related("job")
            .first()
        )

        # Handle case where user has no job yet
        if not primary_job:
            context.update({
                "profile": profile,
                "primary_job": None,
                "error": "You have not been assigned a job yet. Please contact your manager.",
                "exams": [],
                "passed_exams": [],
                "failed_exams": [],
                "remaining_exams": [],
                "total_exams": 0,
                "taken_count": 0,
                "passed_count": 0,
                "failed_count": 0,
                "remaining_count": 0,
            })
            return context

        # All exams for this user's job
        exams = Exam.objects.filter(job=primary_job.job)

        # Get user's latest results (handle retakes)
        latest_results = (
            ExamResult.objects.filter(profile=profile)
            .order_by('exam_id', '-submitted_at')
        )
        result_dict = {}
        for r in latest_results:
            result_dict.setdefault(r.exam_id, r)  # keep latest per exam

        # Split exams by result type
        taken_exams, passed_exams, failed_exams, remaining_exams = [], [], [], []

        for exam in exams:
            result = result_dict.get(exam.id)
            if result:
                taken_exams.append(exam)
                if result.passed:
                    passed_exams.append(exam)
                else:
                    failed_exams.append(exam)
            else:
                remaining_exams.append(exam)

        # Stats
        total_exams = exams.count()
        taken_count = len(taken_exams)
        passed_count = len(passed_exams)
        failed_count = len(failed_exams)
        remaining_count = len(remaining_exams)

        context.update({
            'profile': profile,
            'primary_job': primary_job.job,
            'exams': exams,
            'passed_exams': passed_exams,
            'failed_exams': failed_exams,
            'remaining_exams': remaining_exams,
            'total_exams': total_exams,
            'taken_count': taken_count,
            'passed_count': passed_count,
            'failed_count': failed_count,
            'remaining_count': remaining_count,
        })
        return context
