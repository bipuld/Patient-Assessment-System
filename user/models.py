from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    GENDER_CHOOSE = (('male', 'Male'), ('female', 'Female'), ('other', 'Others'))
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="marketing_app_user", primary_key=True) # first create the user then create the user info create user through the python manage.py createsuperuser cmd
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOOSE, default="male")
    phone = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone.help_text = "if has more than one no write separated with comma."
    is_verify = models.BooleanField(default=False)
    email = models.EmailField()

    @property
    def full_name(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}"
        else:
            return None
        
    def __str__(self):
        if self.user:
            return f"{self.user.id} - {self.first_name}- {self.user.email}"
        else:
            return "Anonymous User"