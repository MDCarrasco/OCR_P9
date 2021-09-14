import unittest.mock

from django import test
from unittest.mock import patch
from django.contrib.auth.models import User

from app.forms import UserCreateForm
from app.views import SignUp


# Create your tests here.
class AuthTester(test.TestCase):

    # @patch("time.time", return_value="")
    @patch("app.views", RequestContext=unittest.mock.Mock())
    def test_sign_up_good(self, mock_request):
        sign_up_form = UserCreateForm(data={
            "username": "test_user",
            "email": "test_user@gmail.com",
            "password1": "12345",
            "password2": "12345"
        })
        # sign_up_form.username = "test_user"
        # sign_up_form.email = "test_user@gmail.com"
        # sign_up_form.password1 = "12345"
        # sign_up_form.password2 = "12345"

        sign_up_view = SignUp()
        sign_up_view.request = mock_request
        sign_up_view.form_valid(sign_up_form)

        expected_user = User.objects.create(username="test_user")
        expected_user.email = "test_user@gmail.com"
        expected_user.set_password("12345")
        expected_user.save()

        user = User.objects.get(username="test_user")

        self.assertEqual(user.email, expected_user.email)
        self.assertTrue(user.check_password("12345"))

    def test_log_in_good(self):
        user = User.objects.create(username="test_user")
        user.set_password("12345")
        user.save()

        client = test.Client()
        logged_in = client.login(username="test_user", password="12345")

        self.assertTrue(logged_in)
