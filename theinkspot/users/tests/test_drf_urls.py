import pytest
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


def test_user_register_url():
    assert reverse("drf-users:register") == "/api/users/register/"
    assert resolve("/api/users/register/").view_name == "drf-users:register"


def test_verify_email_url():
    assert reverse("drf-users:verify-email") == "/api/users/verify-email/"
    assert resolve("/api/users/verify-email/").view_name == "drf-users:verify-email"
