import jwt
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from config.settings.local import SECRET_KEY
from theinkspot.users.models import User

pytestmark = pytest.mark.django_db
client = APIClient()


@pytest.mark.django_db
class TestRegisterView:
    def test_register_user_valid_data(self):
        data = {
            "name": "nancy farid",
            "username": "nancy_farid_1",
            "email": "nancyfarid1@gmail.com",
            "password": "Nan123456789555Far",
            "password_confirmation": "Nan123456789555Far",
        }
        response = client.post("/api/users/register/", data)
        payload = response.data
        assert response.status_code == 201
        assert payload["name"] == data["name"]
        assert payload["email"] == data["email"]
        user = User.objects.filter(username="nancy_farid_1").first()
        assert user is not None
        assert user.email == "nancyfarid1@gmail.com"

    def test_register_user_with_empty_name(self):
        data = {
            "name": "",
            "username": "nancy_farid_1",
            "email": "nancyfarid1@gmail.com",
            "password": "Nan123456789555Far",
            "password_confirmation": "Nan123456789555Far",
        }

        response = client.post("/api/users/register/", data)
        assert response.status_code == 400

    def test_register_user_with_name_len_less_than_8(self):
        data = {
            "name": "nancy",
            "username": "nancy_farid_1",
            "email": "nancyfarid1@gmail.com",
            "password": "Nan123456789555Far",
            "password_confirmation": "Nan123456789555Far",
        }
        response = client.post("/api/users/register/", data)
        assert response.status_code == 400

    def test_register_user_with_empty_username(self):
        data = {
            "name": "nancy farid",
            "username": "",
            "email": "nancyfarid1@gmail.com",
            "password": "Nan123456789555Far",
            "password_confirmation": "Nan123456789555Far",
        }

        response = client.post("/api/users/register/", data)
        assert response.status_code == 400

    def test_register_user_with_username_len_less_than_8(self):
        data = {
            "name": "nancy farid",
            "username": "nancy_1",
            "email": "nancyfarid1@gmail.com",
            "password": "Nan123456789555Far",
            "password_confirmation": "Nan123456789555Far",
        }
        response = client.post("/api/users/register/", data)
        assert response.status_code == 400

    def test_register_user_with_username_already_exists(self, user):
        data = {
            "name": "nancy farid",
            "username": "username",
            "email": "nancyfarid1@gmail.com",
            "password": "Nan123456789555Far",
            "password_confirmation": "Nan123456789555Far",
        }
        response = client.post("/api/users/register/", data)
        assert response.status_code == 400

    def test_register_empty_email(self):
        data = {
            "name": "nancy farid",
            "username": "nancy_farid_1",
            "email": "",
            "password": "Nan123456789555Far",
            "password_confirmation": "Nan123456789555Far",
        }
        response = client.post("/api/users/register/", data)
        assert response.status_code == 400

    def test_register_user_with_invalid_email_format(self):
        data = {
            "name": "nancy farid",
            "username": "nancy_farid_1",
            "email": "nancyfa.o",
            "password": "Nan123456789555Far",
            "password_confirmation": "Nan123456789555Far",
        }
        response = client.post("/api/users/register/", data)
        assert response.status_code == 400

    def test_register_user_with_email_already_exists(self):
        data = {
            "name": "nancy",
            "username": "nancy_farid_1",
            "email": "user@email.com",
            "password": "Nan123456789555Far",
            "password_confirmation": "Nan123456789555Far",
        }
        _ = User.objects.create_user(
            "nancy farid", "nancy_farid_1", "user@email.com", "Nan123456789555Far"
        )
        response = client.post("/api/users/register/", data)
        assert response.status_code == 400

    def test_register_user_with_no_password(self):
        data = {
            "name": "nancy",
            "username": "nancy_farid_1",
            "email": "nancyfarid1@gmail.com",
            "password": "",
            "password_confirmation": "Nan123456789555Far",
        }
        response = client.post("/api/users/register/", data)
        assert response.status_code == 400

    def test_register_user_with_no_password_confirmation(self):
        data = {
            "name": "nancy",
            "username": "nancy_farid_1",
            "email": "nancyfarid1@gmail.com",
            "password": "Nan123456789555Far",
            "password_confirmation": "",
        }
        response = client.post("/api/users/register/", data)
        assert response.status_code == 400

    def test_register_user_with_password_min_len(self):
        data = {
            "name": "nancy farid",
            "username": "nancy_farid_1",
            "email": "nancyfarid1@gmail.com",
            "password": "Nan123456",
            "password_confirmation": "Nan123456",
        }
        response = client.post("/api/users/register/", data)
        assert response.status_code == 400

    def test_register_user_with_password_max_len(self):
        data = {
            "name": "nancy farid",
            "username": "nancy_farid_1",
            "email": "nancyfarid1@gmail.com",
            "password": 40 * "Na12",
            "password_confirmation": "Nan123456789555Far",
        }
        response = client.post("/api/users/register/", data)
        assert response.status_code == 400

    def test_register_user_diffrant_passwords(self):
        data = {
            "name": "nancy",
            "username": "nancy_farid_1",
            "email": "nancyfarid1@gmail.com",
            "password": "Nan123456789555Far",
            "password_confirmation": "Far123456789555Nan",
        }
        response = client.post("/api/users/register/", data)
        assert response.status_code == 400

    def test_register_user_with_invalid_passwords(self):
        data = {
            "name": "nancy farid",
            "username": "nancy_farid_1",
            "email": "nancyfarid1@gmail.com",
            "password": "123456789555",
            "password_confirmation": "Far123456789555Nan",
        }
        response = client.post("/api/users/register/", data)
        assert response.status_code == 400


@pytest.mark.django_db
class TestVerificatinMailView:
    def test_successfull_account_activation_exist_user(self, user):
        token = RefreshToken.for_user(user).access_token
        relative_link = reverse("api-users:verify-email")
        url = f"{relative_link}?token={token}"
        request = client.get(url)
        assert request.status_code == 200
        # hard refresh the object from db
        user = User.objects.get(id=user.pk)
        assert user.is_verified is True

    def test_successfull_account_activation_invalid_token(self, user):
        token = jwt.encode({"user_id": user.id}, SECRET_KEY, algorithm="HS256")
        relative_link = reverse("api-users:verify-email")
        url = f"{relative_link}?token={token}"
        request = client.get(url)
        assert request.status_code == 401
        # hard refresh the object from db
        user = User.objects.get(id=user.id)
        assert user.is_verified is False

    def test_successfull_account_activation_for_non_existing_user(self):
        token = jwt.encode({"user_id": 562}, SECRET_KEY, algorithm="HS256")
        relative_link = reverse("api-users:verify-email")
        url = f"{relative_link}?token={token}"
        request = client.get(url)
        assert request.status_code == 401
