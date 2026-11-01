
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import JobApplication


class HomePageTest(TestCase):

    # Test 1: Dashboard loads after login
    def test_home_page_loads(self):

        User.objects.create_user(
            username='testuser',
            password='TestPassword123'
        )

        self.client.login(
            username='testuser',
            password='TestPassword123'
        )

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)

    # Test 2: User registration works
    def test_user_registration(self):

        response = self.client.post(
            reverse('register'),
            {
                'username': 'newuser',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            User.objects.filter(username='newuser').exists()
        )

    # Test 3: Job application creation works
    def test_add_job_application(self):

        user = User.objects.create_user(
            username='jobuser',
            password='TestPassword123'
        )

        self.client.login(
            username='jobuser',
            password='TestPassword123'
        )

        response = self.client.post(
            reverse('add_job'),
            {
                'company_name': 'ABC Technologies',
                'job_role': 'Python Developer',
                'location': 'Chennai',
                'applied_date': '2026-11-01',
                'status': 'Applied',
                'job_link': 'https://example.com',
                'notes': 'Django testing'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            JobApplication.objects.filter(
                user=user,
                company_name='ABC Technologies'
            ).exists()
        )
