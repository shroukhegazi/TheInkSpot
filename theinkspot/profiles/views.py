from rest_framework import generics, mixins, status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from theinkspot.users.models import User

from .models import Profile
from .permissions import OwnProfilePermission
from .serializers import ChangePasswordSerializer, ProfileSerializer


class ProfileModelViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = (
                IsAuthenticated,
                OwnProfilePermission,
            )
        return [permission() for permission in permission_classes]


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (OwnProfilePermission,)

    def update(self, request, *args, **kwargs):
        self.object = request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
