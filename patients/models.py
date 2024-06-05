from django.db import models
from django.contrib.auth.models import User
from user.models import UserInfo

class Patient(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]

    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    created_date=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(UserInfo,on_delete=models.PROTECT,null=True,db_column="created_by",related_name="+")
    updated_at=models.DateTimeField(auto_now_add=True)

    @property  #this let us to define custom behavior for getting and setting attributes on instances of a class.
    def age(self):
        from datetime import date
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age