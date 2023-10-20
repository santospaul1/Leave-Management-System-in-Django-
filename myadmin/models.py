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


class Employee(models.Model):
    empcode = models.CharField(max_length=50)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    mobileno = models.CharField(max_length=10)
    status = models.IntegerField(default=1)


class LeaveType(models.Model):
    LeaveType = models.CharField(max_length=255)
    Description = models.TextField()
    EmpId = models.CharField(max_length=10, default='default_value')
    FirstName = models.CharField(max_length=100, default='Paul')
    LastName = models.CharField(max_length=100, default='Santos')
    PostingDate = models.DateField(auto_now_add=True)
    Status = models.IntegerField(default=0)

    def __str__(self):
        return self.LeaveType


class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    EmpId = models.CharField(max_length=10, default='default_value')
    leave_type = models.CharField(max_length=100, default='Annual')
    posting_date = models.DateField(auto_now_add=True)
    status = models.IntegerField(default=1)
