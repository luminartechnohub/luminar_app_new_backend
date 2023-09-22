from django.db import models
from account.models import Student

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=100,unique=True)
    description = models.TextField()
    duration=models.CharField(max_length=300,default="6 months")
    offline_fees = models.DecimalField(max_digits=10, decimal_places=2)
    online_fees = models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail = models.ImageField(upload_to='thumbnails',null=True,blank=True)
    full_name=models.CharField(max_length=100,default=False) 
    cochin_date = models.CharField(max_length=50,null=True,blank=True)
    calicut_date = models.CharField(max_length=50,null=True,blank=True)
    offline_choise=((
        'True','True'),
        ('False','False'))
    offline_active = models.CharField(max_length=20,default='False', choices=offline_choise)
    online_choise=((
        'True','True'),
        ('False','False'))
    online_active = models.CharField(max_length=20,default='False', choices=online_choise,)
    is_active = models.BooleanField(default=True)

    @property
    def modules(self):
        return Module.objects.filter(course=self)

    def __str__(self):
        return self.title
    
    # def modules(self):
       
    #     return self.module_set.all()

class Module(models.Model):
    course=models.ForeignKey(Course,on_delete=models.DO_NOTHING, null=True, blank=True)
    mod_no=models.CharField(max_length=100,null=True)
    mod_heading=models.CharField(max_length=100)
    mod_description=models.CharField(max_length=1000)  

    

    def __str__(self):
        return self.mod_heading     


class Batch(models.Model):
    batch_name=models.CharField(max_length=100,unique=True)
    course=models.ForeignKey(Course,on_delete=models.DO_NOTHING,null=True,blank=True)
    startdate=models.CharField(max_length=100)
    time=models.CharField(max_length=50,null=True,blank=True)
    is_active=models.BooleanField(default=True)
    students=models.ManyToManyField(Student,related_name='batch',blank=True)
    
    def __str__(self):
        return self.batch_name        