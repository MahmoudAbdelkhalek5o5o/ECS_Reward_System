from django.contrib.auth.models import AbstractUser

from django.db import models
from enum import Enum
from PIL import Image


class Role(Enum):
     A = "Admin"
     M = "Manager"
     E = "Employee"

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(null = False, blank = False , unique = True)
    emp_id = models.IntegerField(null = False, blank = False , primary_key= True, unique = True,default=3324)
    img = models.ImageField(upload_to='images/', null = True , blank = True, default = 'images/plus.png')
    role = models.CharField(max_length=10, null = False , blank = False, choices=[(tag, tag.value) for tag in Role],default=Role.A)
    phone_number = models.CharField(null = False, blank= False, max_length= 20,default ='01001234567')
    points = models.IntegerField(default=0)
    is_archived = models.BooleanField(null=False , default = False)
    

    

    
    def __str__(self):
        return f"{self.username} {self.role}"
    
class announcements(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE,null=False , blank = False)
    PostText= models.CharField(max_length=1024,null=False, blank= False)
    StartDate= models.DateTimeField(auto_now_add=True,editable=False)
    EndDate=models.DateTimeField(editable=False)
    is_archived = models.BooleanField(null=False , default = False)

class UserRegisterationRequests(models.Model):
    username = models.CharField(max_length=20, null = False , blank = False)
    first_name = models.CharField(max_length=20, null = False , blank = False)
    last_name = models.CharField(max_length=20, null = False , blank = False)
    password = models.CharField(max_length=100, null = False , blank = False, default='123456Abc')
    email = models.EmailField(null = False, blank = False)
    emp_id = models.IntegerField(null = False, blank = False , primary_key= True, unique = True)
    img = models.ImageField(upload_to='images/', null = True , blank = True, default = 'Logo.png')
    role = models.CharField(max_length=10, null = False , blank = False, choices=[(tag, tag.value) for tag in Role])
    phone_number = models.CharField(null = False, blank= False, max_length= 20,default ='01001234567')
    is_archived = models.BooleanField(null=False , default = False)


    
    
    
    
    
    
    
    
    