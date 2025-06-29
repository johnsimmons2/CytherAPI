import logging
from django.utils.timezone import now
from ..models.user import User


logger = logging.getLogger(__file__) # __file__ or __name__?

def get_all():
    return User.objects.all()

def get(id: str):
    try:
        return User.objects.get(id=id)
    except User.DoesNotExist:
        return None

def get_by_username(username: str) -> User | None:
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None

def get_by_email(email: str) -> User | None:
    try:
        return User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None

def update_password(user_id: int, new_password: str) -> User | None:
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None
    
    user.set_password(new_password)
    user.last_login = now()
    user.save()
    return user

def update_user(user_id: int, new_data: dict) -> User | None:
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None
    
    user.email = new_data.get('email', user.email.lower())
    user.username = new_data.get('username', user.username)
    user.first_name = new_data.get('fName', user.fName)
    user.last_name = new_data.get('lName', user.lName)
    user.is_active = new_data.get('is_active', user.is_active)
    user.is_staff = new_data.get('is_staff', user.is_staff)
    user.is_superuser = new_data.get('is_superuser', user.is_superuser) 
    
    user.last_login = now()
    user.save()
    return user