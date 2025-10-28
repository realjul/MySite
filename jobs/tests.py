from django.test import TestCase
from accounts.models import Profile
from jobs.models import JobBase, EmployeeJob
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.
class JobBaseModelTests(TestCase):
    def setUp(self):
        self.job = JobBase.objects.create(title="Manager", description="Be a leader")

    def test_job_title(self):
        """ JobBase object should be created correctly """
        self.assertEqual(self.job.title, "Manager")
        self.assertEqual(self.job.description, "Be a leader")

class EmployeeJobModelTests(TestCase):

    def setUp(self):
        # Create user and profile
        self.user = User.objects.create_user(username='testuser', email='test@email.com', password='testpass123')
        self.profile = Profile.objects.get(user=self.user)
        # Create Job
        self.job = JobBase.objects.create(title="Manager", description="Be a leader")
        # Link them
        self.employee_job = EmployeeJob.objects.create(profile=self.profile, job=self.job,is_primary=True)

    def test_employeejob_creation(self):
        """ EmployeeJob should link a profile and job """
        self.assertEqual(self.employee_job.profile.user.username, "testuser")
        self.assertEqual(self.employee_job.job.title, "Manager")

    def test_employeejob_str_method(self):
        """ EmployeeJob str method should return job title """
        self.assertEqual(str(self.employee_job),"testuser - Manager")

    def test_unique_together_constraint(self):
        """ Duplicate profile-job pair should raise IntegrityError """
        from django.db.utils import IntegrityError
        with self.assertRaises(IntegrityError):
            EmployeeJob.objects.create(profile=self.profile, job=self.job, is_primary=True)