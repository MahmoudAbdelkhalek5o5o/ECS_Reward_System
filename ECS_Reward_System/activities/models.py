from django.db import models
from Users.models import User, Role
from enum import Enum

# Create your models here.

class Status(Enum):
    A = "Approved"
    P = "Pending"
    D = "Declined"

class ActivityCategory(models.Model):
    category_name = models.CharField(max_length=30,null=False, blank= False, unique = True)
    description =  models.CharField(max_length=255,null=False, blank= False, default="")
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True)
    end_date = models.DateTimeField(editable=True , null = True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=False , blank = False)
    budget = models.IntegerField(null = False, blank = False)
    budget_compare = models.IntegerField(null = False, blank = False)
    is_archived = models.BooleanField(null=False , default=False)
    # def __str__(self):
    #     return f"{self.category_name}"

class Activity(models.Model):
    activity_name = models.CharField(max_length=30,null=False, blank= False, unique=True)
    activity_description = models.CharField(max_length=1024,null=False, blank= True)
    category = models.ForeignKey(ActivityCategory,on_delete=models.CASCADE,null=False , blank = False)
    points = models.IntegerField(null = False, blank = False)
    attachment_mandatory = models.BooleanField(default=True)
    #approver = models.ForeignKey(User,on_delete=models.CASCADE,null=False , blank = False)
    evidence_needed =  models.CharField(max_length=1024,null=False, blank= False)
    creation_date = models.DateTimeField(auto_now_add=True,editable=False)
    start_date = models.DateTimeField(editable=True)
    end_date = models.DateTimeField(editable=True,null=True)
    is_approved = models.BooleanField(null=False,blank = False , default=False)
    is_archived = models.BooleanField(null=False , default=False)

class ActivityRequest(models.Model):
    emp = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank= False, related_name="submitter", limit_choices_to={'role':Role.E or Role.M}, db_constraint= True)
    submission_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE,  null=False, blank= False, db_constraint= True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE,  null=False, blank= False, db_constraint= True)
    status = models.CharField(max_length=10, null = False , blank = False, choices=[(tag, tag.value) for tag in Status])
    #approved_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null = True, blank = False, related_name="approver", limit_choices_to={'role':Role.A or Role.M}, db_constraint= True)
    evidence_needed = models.CharField(max_length=1024,null=False, blank= False, default="Provide evidence please")
    proof_of_action = models.FileField(upload_to = "proofs/",null=False, blank= False)
    activity_approval_date = models.DateTimeField(auto_now_add=False, auto_now=False, null = True, blank = False)
    is_archived = models.BooleanField(null=False , default = False)
    
    
class ActivitySuggestion(models.Model):
    activity_name = models.CharField(max_length=30 , null = False, blank=False)
    category = models.ForeignKey(ActivityCategory , on_delete=models.CASCADE , null=False , blank = False)
    activity_description = models.CharField(max_length=1024 , null = False, blank=False)
    justification = models.CharField(max_length=30 , null = True, blank=True)
    evidence_needed = models.CharField(max_length=1024 , null = True, blank=True)
    is_archived = models.BooleanField(null=False , default = False)
    
class Points(models.Model):
    points = models.IntegerField(null = False, blank = False)
    amounts = models.IntegerField(null = False, blank = False)
    start_date = models.DateTimeField(auto_now_add=True,editable=False)
    end_date = models.DateTimeField(editable=False)
    employee = models.ForeignKey(User , on_delete=models.CASCADE,null=False , blank = False, related_name="earned_to")
    is_used = models.BooleanField(null=False,blank = False , default=False)
    
    
    
class ActivityCategoryEdit(models.Model):
    original_category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE,null=False , blank = False)
    category_name = models.CharField(max_length=30,null=False, blank= False)
    description =  models.CharField(max_length=255,null=False, blank= False, default="")
    end_date = models.DateTimeField(editable=True , null = True)
    budget = models.IntegerField(null = False, blank = False)
    edited = models.BooleanField(null=False,blank = False , default=False)
    deleted = models.BooleanField(null=False,blank = False , default=False)


class ActivityEdit(models.Model):
    original_activity = models.ForeignKey(Activity, on_delete=models.CASCADE,null=False , blank = False)
    activity_name = models.CharField(max_length=30,null=False, blank= False)
    activity_description = models.CharField(max_length=1024,null=False, blank= True)
    points = models.IntegerField(null = False, blank = False)
    end_date = models.DateTimeField(editable=True,null=True)
    edited = models.BooleanField(null=False,blank = False , default=False)
    deleted = models.BooleanField(null=False,blank = False , default=False)