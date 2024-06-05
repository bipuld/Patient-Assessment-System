from django.db import models
from django.contrib.auth.models import User
from user.models import UserInfo
from ckeditor.fields import RichTextField
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
    def __str__(self):
        return self.full_name

class Clinician(models.Model):
    clincal_user= models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    def __str__(self):
        return self.clincal_user.user.username

class Assessment(models.Model):
    clinician = models.ForeignKey(Clinician, on_delete=models.CASCADE)
    assessment_type = models.CharField(max_length=100)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    assessment_date = models.DateField()
    questions_and_answers = RichTextField()
    final_score = models.FloatField()
    class Meta:
        verbose_name = "Assessment"
        verbose_name_plural = "Assessments"
    
    def __str__(self):
        return f"{self.assessment_type} for {self.patient.full_name}-{self.assessment_date}"