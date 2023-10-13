from django.urls import path

from .views import LoginView, LogoutView, RegisterView, ConfirmEmailView, PasswordResetView, PasswordResetConfirmView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('api/reset/password', PasswordResetView.as_view(), name='reset_password'),
    path('api/reset/password/confirm/<str:token>/', PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path('confirm_email/<str:token>/', ConfirmEmailView.as_view(), name='confirm_email'),
]
