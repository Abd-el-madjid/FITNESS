# backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            print(f"User with email {email} does not exist.")
            return None

        stored_hashed_password = user.password
        print(f"Stored Hashed Password in CustomUserBackend: {stored_hashed_password}")

        if user.check_password(password):
            print(f"User {email} authenticated successfully.")
            return user
        else:
            print(f"User {email} authentication failed. Incorrect password.")
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
