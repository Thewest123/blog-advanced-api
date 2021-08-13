from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.settings import api_settings

from .serializers import ChangePasswordSerializer


class UserLoginView(ObtainAuthToken):
    """
    Generates a new token with provided credentials,
    deletes old token if already present
    """

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if Token.objects.filter(user=user).exists():
            Token.objects.get(user=user).delete()

        token = Token.objects.create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class UserLogoutView(APIView):
    """Deletes the token for authenticated user"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if Token.objects.filter(user=request.user).exists():
            token = request.user.auth_token
            token.delete()
            return Response(
                status=status.HTTP_200_OK,
                data={'detail': 'User\'s token removed successfully!'}
            )
        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'detail': 'The user doesn\'t have any auth tokens!'}
            )


class ChangePasswordView(generics.GenericAPIView):
    """An endpoint for changing password."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
