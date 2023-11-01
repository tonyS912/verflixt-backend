from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework import serializers

from authentication.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'confirm_password', 'first_name', 'last_name')

    def validate(self, attrs):
        """
        Validates if the password and the password match again.

        Args:
            attrs: password and confirm_password

        Returns:
            Attributes

        Raises:
            ValidationError: if password and confirm_password are not equal

        """
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError('Passwords do not match.')
        return attrs

    @staticmethod
    def validate_password(value):
        """
        Validates if the Password is a secure password, comes from Django

        Args:
            value: password itself

        Returns:
            if password is secure or not
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    @staticmethod
    def validate_email(value):
        """
        Validates the email address, if it can a possible email address

        Args:
            value: email itself

        Returns:
            if it is valid or trash one
        """
        email_validator = EmailValidator()
        try:
            email_validator(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email address.")
        return value

    def create(self, validated_data):
        """
        creates a new user

        Args:
            validated_data: confirmed password

        Returns:
            user: created user, uid and token are used for

        """
        del validated_data["confirm_password"]  # remove password from variable
        user = get_user_model().objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        confirmation_token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))  # .decode()
        return {"user": user, "uid": uid, "token": confirmation_token}


class EmailConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()

    @staticmethod
    def validate_token(value):
        """
        Activate the user if Token is correct

        Args:
            value: Token from users email

        Returns:
            activation from user
        """
        for user in get_user_model().objects.filter(is_active=False):
            if default_token_generator.check_token(user, value):
                user.is_active = True
                user.save()
                return value

        raise serializers.ValidationError("Invalid token provided.")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    @staticmethod
    def authenticate_by_email(email, password):
        user = get_user_model()
        try:
            user = user.objects.get(email=email)
            if user.check_password(password):
                return user
        except user.DoesNotExist:
            return None

    def validate(self, attrs):
        user = self.authenticate_by_email(attrs["email"], attrs["password"])

        if user:
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return {'username': user.username, 'token': token.key, 'email': user.email}
            else:
                raise serializers.ValidationError("Please confirm your E-Mail.")
        else:
            raise serializers.ValidationError("Invalid username or password.")


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            get_user_model().objects.get(email=value)
            return value
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

    def save(self):
        email = self.validated_data["email"]
        user = get_user_model().objects.get(email=email)
        token = Token.objects.get_or_create(user=user)
        result = {"token": token, "user": user}
        return result


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def save(self, **kwargs):
        token = self.context["token"]
        user = CustomUser.objects.get(auth_token=token)
        user.set_password(self.validated_data["password"])
        user.save()

    # if default_token_generator.check_token(user, self.validated_data["token"]):
    #     user.set_password(self.validated_data["password"])
    #     user.save()
    #     return {"detail": "Password reset successful."}
    # else:
    #     raise serializers.ValidationError("Invalid token.")
