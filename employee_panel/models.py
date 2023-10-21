# models.py

from django.db import models
from django.contrib.auth.models import User

class Leave(models.Model):
    empid = models.ForeignKey(User, on_delete=models.CASCADE)
    LeaveType = models.CharField(max_length=100)
    FromDate = models.DateField()
    ToDate = models.DateField()
    Description = models.TextField()
    PostingDate = models.DateField()
    AdminRemarkDate = models.DateField()
    AdminRemark = models.TextField()
    Status = models.IntegerField()
    IsRead = models.IntegerField()
class LeaveType(models.Model):
    LeaveType = models.CharField(max_length=100)


