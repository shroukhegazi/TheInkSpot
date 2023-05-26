import datetime as dt
from typing import Dict

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError as DjValidationError
from django.core.mail import EmailMessage, send_mail
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    NotAuthenticated,
    NotFound,
    ParseError,
)
from rest_framework.exceptions import ValidationError as APIValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from theinkspot.category.models import Category
from theinkspot.users.api.serializers import UserSerializer, TestUserSerialzier
from theinkspot.users.models import UserCategoryFollow

User = get_user_model()


class UserCheckViewset(
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet
):
    serializer_class = TestUserSerialzier
    queryset = User.objects.all()
    lookup_field = 'pk'

class RegisterUsers(generics.GenericAPIView):

    serializer_class = UserSerializer

    def post(self, request):

        user = request.data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        # this part needs to move to another flow https://oyasr.atlassian.net/browse/INK-40
        user = User.objects.get(email=user_data["email"])
        token = RefreshToken.for_user(user).access_token
        current_site = "0.0.0.0:8000"
        relative_link = reverse("api-users:verify-email")
        absurl = "http://" + current_site + relative_link + "?token=" + str(token)
        email_body = (
            "Hi "
            + user.name.split(" ")[0]
            + ",\n"
            + "Thank you for registering with us, Please use the link below to verify your email address \n"
            + absurl
        )
        email_subject = "Verify your email address"

        email = EmailMessage(subject=email_subject, body=email_body, to=[user.email])
        email.send()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        obj = JWTAuthentication()
        validated_token = obj.get_validated_token(request.GET["token"])
        user_id = validated_token["user_id"]
        user = User.objects.get(id=user_id)
        if user:

            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response(
                    {"email": "Successfully Activated"}, status=status.HTTP_200_OK
                )
            return Response(
                {"email": "Already Activated"}, status=status.HTTP_400_BAD_REQUEST
            )


class CategoryFollow(GenericViewSet):
    @action(
        methods=["POST"],
        detail=False,
        url_path="follow",
        url_name="follow",
        permission_classes=[IsAuthenticated],
    )
    def follow(self, request):

        category = get_object_or_404(Category, name=request.data.get("category"))

        try:
            follow = UserCategoryFollow.objects.create(
                user=request.user, category=category
            )
            follow.save()
            data = {
                "msg": "followed successfully",
                "category": str(category),
                "user": str(request.user),
                "get_email": str(follow.get_email),
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {"msg": "category already followed"}, status=status.HTTP_409_CONFLICT
            )

    @action(
        methods=["POST"],
        detail=False,
        url_path="unfollow",
        url_name="unfollow",
        permission_classes=[IsAuthenticated],
    )
    def unfollow(self, request):

        category = get_object_or_404(Category, name=request.data.get("category"))

        try:
            follow = UserCategoryFollow.objects.get(
                user=request.user, category=category
            )
            follow.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(
                {"msg": "You are not following this category"},
                status=status.HTTP_409_CONFLICT,
            )

    @action(
        methods=["POST"],
        detail=False,
        url_path="subscribe",
        url_name="get-email",
        permission_classes=[IsAuthenticated],
    )
    def subscribe_category_newsletter(self, request):

        category = get_object_or_404(Category, name=request.data.get("category"))
        object = get_object_or_404(
            UserCategoryFollow, user=request.user, category=category
        )

        if object.get_email:
            return Response(
                {"error": "You alerady subscribing for newsletter for this category"},
                status=status.HTTP_409_CONFLICT,
            )

        object.get_email = True
        object.save()
        return Response({"msg": "Subscribed successfully"}, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=False,
        url_path="unsubscribe",
        url_name="stop-emails",
        permission_classes=[IsAuthenticated],
    )
    def unsubscribe_category_newsletter(self, request):

        category = get_object_or_404(Category, name=request.data.get("category"))
        object = get_object_or_404(
            UserCategoryFollow, user=request.user, category=category
        )

        if not object.get_email:
            return Response(
                {"error": "You are not subscribing for newsletter for this category"},
                status=status.HTTP_409_CONFLICT,
            )

        object.get_email = False
        object.save()
        return Response({"msg": "Unsubscribed successfully"}, status=status.HTTP_200_OK)


class UserViewSet(ViewSet):
    @action(methods=["POST"], detail=False, url_path="forgot-password", permission_classes=[AllowAny],
            throttle_classes=[AnonRateThrottle])  # fmt: skip
    def forgot_password(self, request: Request):
        email = request.data.get("email")
        if not email:
            raise ParseError("Email must be provided!")

        response_msg: str = f"We will send an email to {email}, if this user exists."

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"msg": response_msg})

        exp_in_mins = 60
        payload = {
            "email": email,
            "operation": "reset-password",
            "exp": dt.datetime.now(tz=dt.timezone.utc) + dt.timedelta(minutes=exp_in_mins)
        }  # fmt: skip
        token = jwt.encode(payload, settings.SECRET_KEY)

        frontend_link = "http://localhost:8000/api/users/reset-password"
        reset_password_link = f"{frontend_link}?token={token}"
        email_msg = (
            f"You can use the following link to reset your password during the next {exp_in_mins} minutes.\n"
            f"Link: {reset_password_link}"
        )
        send_mail(subject="Resetting your Password", message=email_msg, from_email="support@theinkspot.com",
                  recipient_list=[email], fail_silently=True)  # fmt: skip

        return Response({"msg": response_msg})

    @action(methods=["POST"], detail=False, url_path="reset-password", permission_classes=[AllowAny],
            throttle_classes=[AnonRateThrottle])  # fmt: skip
    def reset_password(self, request: Request):
        token = request.headers.get("authorization")
        if not token:
            raise NotAuthenticated()

        password = request.data.get("password")
        if not password:
            raise ParseError("Password must be provided!")

        confirmed_password = request.data.get("confirmed_password")
        if not confirmed_password:
            raise ParseError("Confirmed password must be provided!")

        if password != confirmed_password:
            exp = APIValidationError("Password is not equal to confirmed password!")
            exp.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            raise exp

        payload: Dict
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, ["HS256"])
        except jwt.InvalidTokenError:
            raise AuthenticationFailed()
        except jwt.PyJWTError:
            raise APIException()

        email = payload.get("email")
        user: User = User.objects.filter(email=email).first()
        if not user:
            raise NotFound("No user with this email!")

        try:
            validate_password(password, user)
        except DjValidationError as exp:
            exp = APIValidationError(exp.messages)
            exp.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            raise exp

        user.set_password(password)
        user.save()

        msg = "Your password was successfully updated."
        send_mail(subject="Resetting your Password", message=msg, from_email="support@theinkspot.com",
                  recipient_list=[email], fail_silently=True)  # fmt: skip

        return Response({"msg": msg})
