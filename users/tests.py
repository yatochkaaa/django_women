from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class RegisterUserTestCase(TestCase):
    def setUp(self):
        """Set up test data for the test cases."""

        self.data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }

    def test_from_registration_get(self):
        """Test GET request to the registration page."""

        path = reverse("users:register")
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/register.html")

    def test_user_registration_success(self):
        """Test successful user registration."""

        path = reverse("users:register")
        user_model = get_user_model()
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users:login"))
        self.assertTrue(user_model.objects.filter(username="testuser").exists())

    def test_user_registration_password_mismatch(self):
        """Test user registration with mismatched passwords."""

        self.data["password2"] = "differentpassword123"
        path = reverse("users:register")
        user_model = get_user_model()
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Введенные пароли не совпадают.", html=True)
        self.assertTemplateUsed(response, "users/register.html")
        self.assertFalse(user_model.objects.filter(username="testuser").exists())

    def test_user_registration_exists_error(self):
        """Test user registration with an existing username."""

        user_model = get_user_model()
        user_model.objects.create_user(username=self.data['username'])
        path = reverse("users:register")
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Пользователь с таким именем уже существует.", html=True)

    def tearDown(self):
        """Clean up after tests."""
