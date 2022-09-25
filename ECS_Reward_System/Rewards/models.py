from datetime import datetime
from tkinter import CASCADE
from xmlrpc.client import DateTime
from django.db import models
from Users.models import User, Role


from enum import Enum

# Create your models here.

class Status(Enum):
    A = "Approved"
    P = "Pending"
    D = "Declined"
class Vendors(models.Model):
    name = models.CharField(max_length=30,null=False, blank= False, unique = True)
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True , null=False)
    end_date = models.DateTimeField(editable = True , null = True)
    img = models.ImageField(upload_to='images/', null = False , blank = True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE , null = False , blank = False)
    is_archived = models.BooleanField(null=False , default = False)
    
    
class Vouchers(models.Model):
    vendor = models.ForeignKey(Vendors,on_delete=models.CASCADE,null=False , blank = False)
    creation_day = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True)
    end_date = models.DateTimeField(editable=True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE , null = False , blank = False)
    points_equivalent = models.IntegerField(null = False, blank = False)
    is_archived = models.BooleanField(null=False , default = False)
    
class Redemption_Request(models.Model):
    employee = models.ForeignKey(User , on_delete = models.CASCADE ,blank = False, related_name="employee")
    voucher = models.ForeignKey(Vouchers,on_delete=models.CASCADE , null=False , blank=False)
    status = models.CharField(max_length=10, null = False , blank = False, choices=[(tag, tag.value) for tag in Status], default=Status.P)
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True , blank = False,related_name="admin")
    request_date = models.DateTimeField(auto_now_add=True,editable=False)
    approved_date = models.DateTimeField(null=True)
    is_archived = models.BooleanField(null=False , default = False)
    
    
class Suggest_Reward(models.Model):
    vendor = models.CharField(max_length=30,null=False, blank= False, unique = False)
    website = models.CharField(max_length=255,null=False, blank= False, unique = False)
    reason = models.CharField(max_length=1024,null=False, blank= False, unique = False)
    is_archived = models.BooleanField(null=False , default = False)
    
    
    
class budget(models.Model):
    budget = models.IntegerField(null = False, blank = False)
    admin = models.ForeignKey(User, on_delete=models.CASCADE , null=False)
    point = models.IntegerField(null = True, blank = False)
    EGP = models.IntegerField(null = True, blank = False)
    budget_compare = models.IntegerField(null = False, blank = False)
    year = models.IntegerField(null = False , default= datetime.now().year)
    start_date = models.DateTimeField(auto_now_add=True)
    Archived_at = models.DateTimeField(null = True)
    is_active = models.BooleanField(null=False , default=True)
    
    
 
    
    
        