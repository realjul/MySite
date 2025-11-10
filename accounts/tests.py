from django.test import TestCase
# import get user model to test user creation
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from accounts.models import Profile
from django.utils import timezone

from .forms import CustomUserCreationForm
from .views import SignupPageView

User = get_user_model()

# Create your tests here.
class CustomUserTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(username="test",email="test@email.com",password="testpass123")
        self.assertEqual(user.username,"test")
        self.assertEqual(user.email,"test@email.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(username="superadmin",email="superuser@email.com",password="testpass123")
        self.assertEqual(admin_user.username,"superadmin")
        self.assertEqual(admin_user.email,"superuser@email.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

class SignupTests(TestCase):

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(self.response, 'Hi there! I should not be shown here.')

    def test_signup_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_view(self):
        view = resolve('/accounts/signup/')
        self.assertEqual(view.func.__name__, SignupPageView.as_view().__name__)

class ProfileSignalTests(TestCase):

    def test_profile_is_created_when_user_is_created(self):
        """A Profile should be created when a User is created."""
        user = User.objects.create_user(username="testuser",email="test@email.com",password="testpass123")
        self.assertTrue(Profile.objects.filter(user=user).exists())
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user.email,"test@email.com")

    def test_profile_is_saved_when_user_is_saved(self):
        """Saving a User should also be save its related Profile via the signal."""
        user = User.objects.create_user(username="testuser",email="test@email.com",password="testpass123")
        profile = user.profile
        profile.phone = "1234567890"
        profile.save()

        # update something on the user and save - should trigger a signal
        profile.phone = "1111111111"
        profile.save()

        updated_profile = Profile.objects.get(user=user)
        self.assertEqual(updated_profile.phone, "1111111111")


    def test_profile_str_method(self):
        """Profile str method should return a string representation of the Profile."""

        user = User.objects.create_user(username="testuser",email="test@email.com",password="testpass123")
        profile = Profile.objects.get(user=user)
        self.assertEqual(str(profile), "testuser's")