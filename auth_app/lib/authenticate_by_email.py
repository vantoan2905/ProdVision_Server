from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

def authenticate_by_email(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    if user.check_password(password):
        return user
    return None
