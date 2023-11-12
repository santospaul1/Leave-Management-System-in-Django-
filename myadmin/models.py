import datetime

from django.contrib.auth.models import User
from django.db import models
from datetime import date


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=100, unique=True)
    CreationDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username


class Department(models.Model):

    department_name = models.CharField(max_length=255)
    department_shortname = models.CharField(max_length=50)
    department_code = models.CharField(max_length=10)
    CreationDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.department_name

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)
EMP_CHOICES = (
        ( 'Active', 'Active'),
        ( 'Inactive', 'Inactive'),
        )
UN_CHOICES = (
    ('Union', 'Union'),
    ('Non-Union', 'Non-Union'),
    ('Others', 'Others')

)
class Employee(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    empcode = models.CharField(max_length=10, primary_key=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=255)

    employee_type = models.CharField(
        max_length=10,
        choices=UN_CHOICES,
        default='Non-Union'
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='Male'
    )
    dob = models.DateField(auto_now_add=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, default="80100")
    city = models.CharField(max_length=100, default="Mombasa")
    country = models.CharField(max_length=100)
    mobileno = models.CharField(max_length=10)
    status = models.CharField(
        max_length=10,
        choices=EMP_CHOICES,
        default='Active'
    )
    CreationDate = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.empcode} - {self.firstName} {self.lastName}"


class LeaveType(models.Model):
    leavetype = models.CharField(max_length=255)
    Description = models.TextField()

    PostingDate = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.leavetype

STATUS_CHOICES = (
        (0, 'Pending'),
        (1, 'Approved'),
        (2, 'Declined')
    )
class Leave(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)

    leave_type = models.CharField(max_length=100, default='Annual')
    posting_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    leavetype = models.CharField(max_length=255, default=None)
    description = models.TextField(default=None)
    fromdate = models.DateField( default=None)
    todate = models.DateField( default=None)
    isread = models.IntegerField(default=0)
    admin_remark = models.CharField(max_length=255, default=None, null=True)


 # You can use your custom User model if you have one

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
