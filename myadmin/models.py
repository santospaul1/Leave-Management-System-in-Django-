from django.contrib.auth.models import User
from django.db import models


class Admin(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=100)

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
class Employee(models.Model):
    empcode = models.CharField(max_length=50)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='Male'
    )
    dob = models.DateField(auto_now_add=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, default="800100")
    city = models.CharField(max_length=100, default="Mombasa")
    country = models.CharField(max_length=100)
    mobileno = models.CharField(max_length=10)
    status = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.empcode} - {self.firstName} {self.lastName}"


class LeaveType(models.Model):
    LeaveType = models.CharField(max_length=255)
    Description = models.TextField()

    PostingDate = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.LeaveType

STATUS_CHOICES = (
        (0, 'Pending'),
        (1, 'Approved'),
        (2, 'Declined')
    )
class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    EmpId = models.CharField(max_length=10, default='default_value')
    leave_type = models.CharField(max_length=100, default='Annual')
    posting_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Pending'
    )

 # You can use your custom User model if you have one

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
