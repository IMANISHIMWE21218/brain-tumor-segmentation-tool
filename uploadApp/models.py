from django.contrib.auth.models import AbstractUser
from django.db import models


class Hospital(models.Model):
    hospital_name = models.CharField(max_length=150)
    hospital_address = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.hospital_name


class User(AbstractUser):
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     self.set_password(self.password)
    #     super(User, self).save(*args, **kwargs)


class Patient(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    original_image = models.ImageField(upload_to="Original_images/")
    result_image = models.ImageField(upload_to="Result_images/", null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{str(self.email)} - {self.created_on}'


class PatientReport(models.Model):
    patientScan = models.ForeignKey(Patient, related_name='comments', on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now=True)
    doctor_comment = models.TextField()
