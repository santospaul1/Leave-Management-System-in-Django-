from django import forms
from .models import LeaveType, Employee, Department, Admin, EMP_CHOICES


EMP_CHOICES = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
)

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'empcode',
            'firstName',
            'lastName',
            'email',
            'password',
            'gender',
            'department',
            'address',
            'city',
            'country',
            'mobileno',
            'status',
        ]





class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = ['leavetype', 'Description']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name', 'department_shortname', 'department_code']
class EmployeeUpdateForm(forms.ModelForm):

  class Meta:
    model = Employee
    fields = ['firstName', 'lastName', 'gender', 'mobileno',
              'address', 'city', 'country', 'department']
class AdminForm:
    class meta:
        model = Admin
        fields = ['fullname', 'email', 'password', 'username']
