from django.contrib.auth import login, logout
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserLoginSerializer, UserPasswordChangeSerializer, UserRegisterSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User
    serializer_class = UserRegisterSerializer


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        login(request, user)

        return Response(serializer.validated_data["tokens"])


class UserLogoutView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"detail": "Logged out successfully."})


class UserPasswordChangeView(generics.GenericAPIView):
    serializer_class = UserPasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        return Response({"detail": "successfully password change"})


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UserRegisterSerializer)
    def put(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
