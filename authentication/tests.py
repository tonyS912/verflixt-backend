from django.conf import settings
from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.models import AnonymousUser, User
from django.db import IntegrityError
from django.http import HttpRequest
from django.test import TestCase, Client, override_settings

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from.models import CustomUser


class BasicTestCase(TestCase):
    def test_user(self):
        """Users can be created and can set their password"""
        u = CustomUser.objects.create_user("testuser", "test@example.com", "testpw")
        self.assertTrue(u.has_usable_password())
        self.assertFalse(u.check_password("bad"))
        self.assertTrue(u.check_password("testpw"))

        # Check we can manually set an unusable password
        u.set_unusable_password()
        u.save()
        self.assertFalse(u.check_password("testpw"))
        self.assertFalse(u.has_usable_password())
        u.set_password("testpw")
        self.assertTrue(u.check_password("testpw"))
        u.set_password(None)
        self.assertFalse(u.has_usable_password())

        # Check username getter
        self.assertEqual(u.get_username(), "testuser")

        # Check authentication/permissions
        self.assertFalse(u.is_anonymous)
        self.assertTrue(u.is_authenticated)
        self.assertFalse(u.is_staff)
        self.assertTrue(u.is_active)
        self.assertFalse(u.is_superuser)

        # Check API-based user creation with no password
        u2 = CustomUser.objects.create_user("testuser2", "test2@example.com")
        self.assertFalse(u2.has_usable_password())

    def test_unicode_username(self):
        CustomUser.objects.create_user("jörg")
        CustomUser.objects.create_user("Григорий")
        # Two equivalent Unicode normalized usernames are duplicates.
        omega_username = "iamtheΩ"  # U+03A9 GREEK CAPITAL LETTER OMEGA
        ohm_username = "iamtheΩ"  # U+2126 OHM SIGN
        CustomUser.objects.create_user(ohm_username)
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(omega_username)

    def test_user_no_email(self):
        """Users can be created without an email"""
        cases = [
            {},
            {"email": ""},
            {"email": None},
        ]
        for i, kwargs in enumerate(cases):
            with self.subTest(**kwargs):
                u = CustomUser.objects.create_user("testuser{}".format(i), **kwargs)
                self.assertEqual(u.email, "")

    def test_superuser(self):
        """Check the creation and properties of a superuser"""
        super = CustomUser.objects.create_superuser("super", "super@example.com", "super")
        self.assertTrue(super.is_superuser)
        self.assertTrue(super.is_active)
        self.assertTrue(super.is_staff)

    def test_superuser_no_email_or_password(self):
        cases = [
            {},
            {"email": ""},
            {"email": None},
            {"password": None},
        ]
        for i, kwargs in enumerate(cases):
            with self.subTest(**kwargs):
                superuser = CustomUser.objects.create_superuser("super{}".format(i), **kwargs)
                self.assertEqual(superuser.email, "")
                self.assertFalse(superuser.has_usable_password())

    def test_get_user_model(self):
        """The current user model can be retrieved"""
        self.assertEqual(get_user_model(), CustomUser)


class TestGetUser(TestCase):
    def test_get_user_anonymous(self):
        request = HttpRequest()
        request.session = self.client.session
        user = get_user(request)
        self.assertIsInstance(user, AnonymousUser)
        print("No Anonymous User can Log-in.")

    def test_get_user(self):
        created_user = CustomUser.objects.create_user(
            "testuser", "test@example.com", "testpw"
        )
        self.client.login(username="testuser", password="testpw")
        request = HttpRequest()
        request.session = self.client.session
        user = get_user(request)
        self.assertIsInstance(user, CustomUser)
        self.assertEqual(user.username, created_user.username)

    def test_get_user_fallback_secret(self):
        created_user = CustomUser.objects.create_user(
            "testuser", "test@example.com", "testpw"
        )
        self.client.login(username="testuser", password="testpw")
        request = HttpRequest()
        request.session = self.client.session
        prev_session_key = request.session.session_key
        with override_settings(
                SECRET_KEY="newsecret",
                SECRET_KEY_FALLBACKS=[settings.SECRET_KEY],
        ):
            user = get_user(request)
            self.assertIsInstance(user, CustomUser)
            self.assertEqual(user.username, created_user.username)
            self.assertNotEqual(request.session.session_key, prev_session_key)
        # Remove the fallback secret.
        # The session hash should be updated using the current secret.
        with override_settings(SECRET_KEY="newsecret"):
            user = get_user(request)
            self.assertIsInstance(user, CustomUser)
            self.assertEqual(user.username, created_user.username)


class RegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.data = {
            "username": "TesterMann",
            "email": "klausdieter@trash-mail.com",
            "password": "schwinz123!",
            "confirm_password": "schwinz123!",
            "first_name": "Klaus",
            "last_name": "Schmidt"
        }

        self.user = CustomUser.objects.create_user(email=self.data["email"], password=self.data["password"],
                                                   username="Hans")
        self.token = Token.objects.create(user=self.user)

    def test_registry(self):
        self.client = Client()

        response = self.client.post('/authentication/register/', self.data)
        print(response.content)
        self.assertEqual(response.status_code, 200)
        print(response.status_code)

    # TODO whats wrong with it
    """
    def test_verification(self):
        print(self.token)
        verification_url = f'http://127.0.0.1:8000/authentication/confirm_email/{self.token}/'
        print(verification_url)
        response = self.client.get(verification_url)
        print(response.content)
        self.assertEqual(response.status_code, 200)
    """


class LoginTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {
            "username": "TesterMan",
            "email": "klausdieter@trash-mail.com",
            "password": "schwinz123!",
        }

        self.user = CustomUser.objects.create_user(email=self.data["email"], password=self.data["password"], username="Hans")
        self.token = Token.objects.create(user=self.user)

    def test_login_user(self):
        self.client = Client()
        self.user.is_active = True
        self.user.save()
        response = self.client.post('/authentication/login/', self.data)
        print(response.content)
        self.assertEqual(response.status_code, 200)
        print(response.status_code)

    def test_login_user_inactive(self):
        self.client = Client()
        self.user.is_active = False
        self.user.save()
        response = self.client.post('/authentication/login/', self.data)
        print(response.content)
        self.assertEqual(response.status_code, 401)
        print(response.status_code)
