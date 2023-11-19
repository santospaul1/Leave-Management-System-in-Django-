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
              'address', 'city', 'country', 'department', 'status']
class AdminForm:
    class meta:
        model = Admin
        fields = ['fullname', 'email', 'password', 'username']
class LeaveActionForm(forms.Form):
    action = forms.ChoiceField(
        choices=((1, 'Approve'), (2, 'Decline')),
        required=True,
        widget=forms.Select(attrs={'class': 'custom-select'}),
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Description', 'maxlength': 500}),
        required=True,
    )
