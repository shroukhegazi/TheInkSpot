from rest_framework import serializers

from theinkspot.users.models import User

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Profile
        fields = [
            "user",
            "about_text",
            "profile_pic",
            "header_pic",
            "short_bio",
            "profile_views",
            "accent_color",
            "background_color",
            "created_at",
            "updated_at",
        ]

    def update(self, instance, validated_data):
        user = self.context["request"].user
        instance.user = validated_data.get(str(user), instance.user)
        instance.about_text = validated_data.get("about_text", instance.about_text)
        instance.profile_pic = validated_data.get("profile_pic", instance.profile_pic)
        instance.header_pic = validated_data.get("header_pic", instance.header_pic)
        instance.short_bio = validated_data.get("short_bio", instance.short_bio)
        instance.profile_views = validated_data.get(
            "profile_views", instance.profile_views
        )
        instance.accent_color = validated_data.get(
            "accent_color", instance.accent_color
        )
        instance.background_color = validated_data.get(
            "background_color", instance.background_color
        )
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Serializer for password change endpoint.
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("old_password", "new_password", "confirm_new_password")

    def validate(self, attrs):
        if attrs["old_password"] != attrs["new_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value
