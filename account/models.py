
# # Create your models here.
from django.contrib.auth.models import AbstractBaseUser,Group
from django.db import models
from .manager import UserManager



class User(AbstractBaseUser):
    full_name=models.CharField(max_length=60,blank=False,null=False)
    phone=models.CharField(max_length=13,blank=False,null=False,unique=True)
    dob=models.CharField(max_length=20,blank=False,null=False)
    email=models.EmailField(max_length=200,null=True,blank=True)
    gender=models.CharField(max_length=20,blank=False,null=False)
    phone_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
        ('student','Student')
    )
    user_type = models.CharField(max_length=20,default='student', choices=ROLE_CHOICES)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.phone}{self.full_name}"

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff


class Student(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    parent_no=models.CharField(max_length=13,blank=False,null=False)
    STATUS_CHOICES = (
        ('waiting', 'Waiting'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')

    def __str__(self):
       return self.user.full_name

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)   



class Admin(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)     


class SuperAdmin(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE) 