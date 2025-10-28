from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Exam, ExamResult, Question, Choice


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
