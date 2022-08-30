from urllib import request

import pytest
from django.core.files import File
from django.test import TestCase
from rest_framework import status

from theinkspot.profiles.models import Profile
from theinkspot.users.models import User

pytestmark = pytest.mark.django_db


class TestProfileViews(TestCase):
    def makeProfile(self):
        self.user = User.objects.create(
            username="test_user",
            email="test_user@dummy.com",
            password="Test_pass123!",
        )
        self.test_img_url = "https://bit.ly/3vQgl0t"
        self.img = request.urlretrieve(self.test_img_url)[0]

        profile = Profile(
            user=self.user,
            about_text="test_about_text",
            short_bio="test_short_bio",
            profile_pic=File(open(self.img, "rb")),
            header_pic=File(open(self.img, "rb")),
        )
        profile.save()
        return profile

    def test_anonymous_user_can_list(self):
        response = self.client.get("/profiles/user-profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_user_can_retrive(self):
        profile = self.makeProfile()
        response = self.client.get("/profiles/user-profile/", args=[profile.id])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_update(self):
        profile = self.makeProfile()
        response = self.client.patch("/profiles/user-profile/", args=[profile.id])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_cannot_delete(self):
        profile = self.makeProfile()
        response = self.client.delete("/profiles/user-profile/", args=[profile.id])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_retrive(self):
        profile = self.makeProfile()
        self.client.force_login(user=profile.user)
        response = self.client.get("/profiles/user-profile/", args=[profile.id])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
