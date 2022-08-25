import pytest
from django.db import IntegrityError

from theinkspot.users.models import User, UserCategoryFollow

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestUserModel:
    def test_update_user(self, user):
        user.name = "mahmoud saeed ali hussain"
        user.save()
        user = User.objects.get(name="mahmoud saeed ali hussain")
        assert user.name == "mahmoud saeed ali hussain"

    def test_filter_user(self, user):
        assert User.objects.filter(username="username").exists()

    def test_object_name_is_first_name(self, user):
        object_name = f"{user.username}"
        assert str(user) == object_name

    def test_object_name_label(self, user):
        name_label = user._meta.get_field("name").verbose_name
        assert name_label == "User Full Name"

    def test_object_email_label(self, user):
        email_label = user._meta.get_field("email").verbose_name
        assert email_label == "Email"

    def test_object_username_label(self, user):
        username_label = user._meta.get_field("username").verbose_name
        assert username_label == "Username"

    def test_object_is_is_verified_label(self, user):
        is_verified_label = user._meta.get_field("is_verified").verbose_name
        assert is_verified_label == "Is user verified by email"

    def test_name_max_length(self, user):
        max_length = user._meta.get_field("name").max_length
        assert max_length == 155

    def test_username_max_length(self, user):
        max_length = user._meta.get_field("username").max_length
        assert max_length == 155

    def test_email_max_length(self, user):
        max_length = user._meta.get_field("email").max_length
        assert max_length == 155

    def test_email_is_unique(self, user):
        is_email_unique = user._meta.get_field("email").unique
        assert is_email_unique is True

    def test_username_is_unique(self, user):
        is_username_unique = user._meta.get_field("username").unique
        assert is_username_unique is True

    def test_is_verified_is_fasle_by_default(self, user):
        is_verified_defaulted_false = user._meta.get_field("is_verified").default
        assert is_verified_defaulted_false is False

    def test_is_superuser_is_false_by_default(self, superuser):
        is_superuser_defaulted_false = superuser._meta.get_field("is_superuser").default
        assert is_superuser_defaulted_false is False

    def test_is_staff_is_false_by_default(self, superuser):
        is_staff_defaulted_false = superuser._meta.get_field("is_staff").default
        assert is_staff_defaulted_false is False

    def test_create_super_user(self, superuser):
        is_user_a_superuser = superuser.is_superuser
        assert is_user_a_superuser is True


@pytest.mark.django_db
class TestUserCategoryFollow:
    def test_user_follow_category(self, user, category):
        follow = UserCategoryFollow.objects.create(user=user, category=category)
        assert user.followers.count() == 1
        assert category.followed_categories.count() == 1
        assert follow.get_email is False

    def test_user_unfollow_category(self, user, category):
        UserCategoryFollow.objects.create(user=user, category=category)
        user.followers.first().delete()
        assert user.followers.count() == 0
        assert category.followed_categories.count() == 0

    def test_user_follow_already_followed_category(self, user, category):
        UserCategoryFollow.objects.create(user=user, category=category)

        with pytest.raises(IntegrityError):
            UserCategoryFollow.objects.create(user=user, category=category)

    def test_user_unfollow_already_unfollowed_category(self, user, category):
        UserCategoryFollow.objects.create(user=user, category=category)
        user.followers.first().delete()

        with pytest.raises(AttributeError):
            user.followers.first().delete()

    def test_custom_model_manager_returns_queryset(self, user, category):
        UserCategoryFollow.objects.create(user=user, category=category)
        object = UserCategoryFollow.objects.first()
        assert object.user == user
        assert object.category == category
