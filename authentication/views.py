from django.contrib.auth import logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from rest_framework import status

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import RegisterSerializer, EmailConfirmSerializer, LoginSerializer, PasswordResetSerializer, \
    PasswordResetConfirmSerializer

from dotenv import load_dotenv
import os

load_dotenv()


class RegisterView(APIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    @staticmethod
    def post(request):
        """
        Register a new user.

        Args:
            request (Request): The HTTP request object containing user registration data.

        Returns:
            Response: A JSON response indicating the result of the registration process.

        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.save()
            confirmation_link = RegisterView._create_confirmation_link(request, user_data['token'])
            email_sender = os.environ.get("EMAIL_SENDER")
            RegisterView._send_confirmation_email(user_data['user'].email, confirmation_link, email_sender)

            return Response({
                "message": 'User has been successfully created, '
                           'Please check your mails to confirm your Registration.'
            })
        else:
            return Response({"error": serializer.errors}, status=400)

    @staticmethod
    def _create_confirmation_link(request, token):
        domain = get_current_site(request).domain
        return f"https://{domain}/authentication/confirm_email/{token}/"

    @staticmethod
    def _send_confirmation_email(email, confirmation_link, email_sender):
        send_mail(
            "Welcome to Verflixt",
            f"Please, follow up this link to confirm the Registration: {confirmation_link}",
            email_sender,
            [email],
            fail_silently=False,
        )


class ConfirmEmailView(APIView):
    @staticmethod
    def get(request, token):
        serializer = EmailConfirmSerializer(data={"token": token})
        if serializer.is_valid():
            return HttpResponseRedirect(os.environ.get("WEB_ADDRESS"))
        else:
            return Response({"error": serializer.errors}, status=401)


class LoginView(APIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @staticmethod
    def post(request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=200)
        else:
            return Response({"error": serializer.errors}, status=401)


class LogoutView(APIView):
    @staticmethod
    def post(request):
        logout(request)
        return Response({"message": "Successfully logged out."}, status=200)


class PasswordResetView(APIView):
    @staticmethod
    def post(request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.save()
            reset_link = PasswordResetView._create_reset_link(request, user_data['token'])
            email_sender = os.environ.get("EMAIL_SENDER")
            PasswordResetView._send_reset_email(user_data['user'].email, reset_link, email_sender)
            return Response({"message": "Password reset email was sendet."}, status=status.HTTP_200_OK)

    @staticmethod
    def _create_reset_link(request, token):
        domain = get_current_site(request).domain
        return f"https://{domain}/authentication/api/reset/password/confirm/{token}/"

    @staticmethod
    def _send_reset_email(email, reset_link, email_sender):
        send_mail(
            "Reset your password",
            f'Click here to reset your password --> <a href="{reset_link}">',
            email_sender,
            [email],
            fail_silently=False,
        )


class PasswordResetConfirmView(APIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetConfirmSerializer

    @staticmethod
    def post(request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.save(), status=200)
        else:
            return Response({"error": serializer.errors}, status=400)
