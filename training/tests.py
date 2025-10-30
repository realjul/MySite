from django.test import TestCase
from django.utils import timezone
from jobs.models import JobBase, Profile
from training.models import Exam, Question, Choice, ExamResult
from django.contrib.auth import get_user_model

User = get_user_model()


class ExamModelTests(TestCase):
    def setUp(self):
        # Create a mock user and profile
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.job = JobBase.objects.create(title="Server", description="Handles guest orders and service.")
        self.profile = Profile.objects.create(user=self.user, job=self.job)

        # Create an exam
        self.exam = Exam.objects.create(
            title="Server Knowledge",
            description="Basic test on restaurant server skills.",
            job=self.job,
            season="FALL",
            year=2025,
            passing_score=90,
            date_created=timezone.now()
        )

        # Create a question and choices
        self.question = Question.objects.create(
            exam=self.exam,
            text="What is the proper temperature for serving steak?",
            order=1
        )

        self.choice1 = Choice.objects.create(question=self.question, text="140°F", is_correct=False)
        self.choice2 = Choice.objects.create(question=self.question, text="155°F", is_correct=True)
        self.choice3 = Choice.objects.create(question=self.question, text="180°F", is_correct=False)

        # Create exam result
        self.result = ExamResult.objects.create(
            profile=self.profile,
            exam=self.exam,
            score=95.0,
            passed=True
        )

def test_exam_creation(self):
    """Ensure exam is created with correct season, year, and job"""
    self.assertEqual(self.exam.title, "Server Knowledge")
    self.assertEqual(self.exam.job.title, "Server")
    self.assertEqual(self.exam.season, "FALL")
    self.assertEqual(self.exam.year, 2025)
    self.assertEqual(str(self.exam), "Server Exam - (Fall 2025)")

def test_question_linked_to_exam(self):
    """Questions should belong to the correct exam"""
    self.assertEqual(self.question.exam, self.exam)
    self.assertEqual(self.question.order, 1)
    self.assertIn("Server Knowledge Q1", str(self.question))

def test_choice_relationships(self):
    """Each choice should belong to the right question"""
    self.assertEqual(self.choice1.question, self.question)
    self.assertTrue(hasattr(self.choice2, "is_correct"))
    self.assertIn("Choice for Q", str(self.choice1))

def test_exam_result_creation(self):
    """ExamResult should link Profile and Exam correctly"""
    self.assertEqual(self.result.profile.user.username, "testuser")
    self.assertEqual(self.result.exam, self.exam)
    self.assertTrue(self.result.passed)
    self.assertAlmostEqual(self.result.score, 95.0, delta=0.1)

def test_exam_unique_together(self):
    """Duplicate exams for same job/season/year should not be allowed"""
    with self.assertRaises(Exception):
        Exam.objects.create(
            title="Duplicate",
            job=self.job,
            season="FALL",
            year=2025
        )

def test_question_ordering(self):
    """Questions should be ordered by 'order' field"""
    q2 = Question.objects.create(exam=self.exam, text="Another question", order=2)
    questions = self.exam.questions.all()
    self.assertEqual(list(questions), [self.question, q2])


# Create your tests here.
