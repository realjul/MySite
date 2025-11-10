from django.test import TestCase
from django.urls import reverse
from accounts.models import Profile
from jobs.models import JobBase, EmployeeJob
from jobs.forms import JobBaseForm, EmployeeJobForm
from django.contrib.auth import get_user_model
from django.utils import timezone

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

class JobBaseViewTests(TestCase):
    def setUp(self):
        # Create user and log them in
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.client.login(username='testuser', password='pass123')

        # Create sample JobBase
        self.job = JobBase.objects.create(title='Server', description='Handles guests.')

    def test_jobbase_list_view(self):
        """List view should return 200 and show the job title"""
        url = reverse('jobbase_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Server')
        self.assertTemplateUsed(response, 'jobs/jobbase_list.html')

    def test_jobbase_create_view(self):
        """Should create a new JobBase"""
        url = reverse('jobbase_create')
        data = {
            'title': 'Cook',
            'description': 'Prepares meals.',
            'department': 'BOH',
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(JobBase.objects.filter(title='Cook').exists())

    def test_jobbase_update_view(self):
        """Should update an existing JobBase"""
        url = reverse('jobbase_update', args=[self.job.id])
        data = {
            'title': 'Server Updated',
            'description': 'Updated desc',
            'department': 'FOH'
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.job.refresh_from_db()
        self.assertEqual(self.job.title, 'Server Updated')

    def test_jobbase_delete_view(self):
        """Should delete a JobBase"""
        url = reverse('jobbase_delete', args=[self.job.id])
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(JobBase.objects.filter(id=self.job.id).exists())