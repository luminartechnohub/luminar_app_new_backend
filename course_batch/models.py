from django.db import models

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
    def __str__(self):
        return self.title
    
    # def modules(self):
       
    #     return self.module_set.all()

class Module(models.Model):
    course=models.ForeignKey(Course,on_delete=models.DO_NOTHING, null=True, blank=True)
    mod_no=models.CharField(max_length=100)
    mod_heading=models.CharField(max_length=100)
    mod_description=models.CharField(max_length=1000)   

    def __str__(self):
        return self.mod_heading     


class Batch(models.Model):
    
    batch_code =models.CharField(max_length=100)
    batch_name=models.CharField(max_length=100,default=True)
    course=models.ForeignKey(Course,on_delete=models.DO_NOTHING,null=True,blank=True)
    startdate=models.CharField(max_length=100,default=True)
    def __str__(self):
        return self.batch_name        