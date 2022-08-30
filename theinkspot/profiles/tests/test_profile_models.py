from urllib import request

import pytest
from django.core.files import File
from django.test import TestCase

from theinkspot.profiles.models import Profile
from theinkspot.users.models import User

pytestmark = pytest.mark.django_db


class ProfileModelTestcase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test_user",
            email="test_user@dummy.com",
            password="Test_pass123!",
        )
        self.test_img_url = "https://bit.ly/3vQgl0t"
        self.img = request.urlretrieve(self.test_img_url)[0]

    def test_create_profile(self):
        profile = Profile(
            user=self.user,
            about_text="test_about_text",
            short_bio="test_short_bio",
            profile_pic=File(open(self.img, "rb")),
            header_pic=File(open(self.img, "rb")),
        )
        profile.save()
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.about_text, "test_about_text")
        self.assertEqual(profile.short_bio, "test_short_bio")
        self.assertEqual(profile.profile_views, 0)
        self.assertEqual(profile.accent_color, "#FFFFFF")
        self.assertEqual(profile.background_color, "#FFFFFF")

    def test_create_profile_with_same_user(self):
        profile = Profile(
            user=self.user,
            about_text="test_about_text",
            profile_pic=File(open(self.img, "rb")),
            header_pic=File(open(self.img, "rb")),
        )
        profile.save()
        with self.assertRaises(Exception):
            self.Profile(
                user=self.user,
                about_text="test_about_text",
                profile_pic=File(open(self.img, "rb")),
                header_pic=File(open(self.img, "rb")),
            )

    def test_create_profile_with_invalid_data(self):
        with self.assertRaises(Exception):
            profile = Profile(
                user=self.user,
                about_text="test_about_text",
                short_bio="test_short_bio",
                profile_pic=File(open(self.img, "rb")),
                header_pic=None,
            )
            profile.save()

    def test_create_profile_with_nonexistentuser(self):
        with self.assertRaises(Exception):
            profile = Profile(
                user=None,
                about_text="test_about_text",
                short_bio="test_short_bio",
                profile_pic=File(open(self.img, "rb")),
                header_pic=File(open(self.img, "rb")),
            )
            profile.save()
