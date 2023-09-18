
# # Create your models here.
from django.contrib.auth.models import AbstractBaseUser,Group
from django.db import models
from .manager import UserManager



class User(AbstractBaseUser):
    full_name=models.CharField(max_length=60,blank=False,null=False)
    course_name=models.CharField(max_length=100,blank=False,null=False)
    parent_no=models.CharField(max_length=13,blank=False,null=False)
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
    user_type = models.CharField(max_length=20, choices=ROLE_CHOICES)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.full_name}"

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration=models.CharField(max_length=300,default="6 months")
    offline_fees = models.DecimalField(max_digits=10, decimal_places=2)
    online_fees = models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail = models.ImageField(upload_to='thumbnails')
    full_name=models.CharField(max_length=100,default=False) 
    cochin=models.CharField(max_length=100,default=False)
    calicut=models.CharField(max_length=100,default=False)
    def __str__(self):
        return self.title
    
    def modules(self):
       
        return self.module_set.all()
    
class Module(models.Model):
    name=models.ForeignKey(Course,on_delete=models.DO_NOTHING, null=True, blank=True)
    mod_no=models.PositiveIntegerField()
    mod_heading=models.CharField(max_length=100)
    mod_description=models.CharField(max_length=1000)

