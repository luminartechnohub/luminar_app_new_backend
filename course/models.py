from django.db import models

# Create your models here.
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


