from django.contrib import admin
from .models import Admin, Department, Leave, Employee, LeaveType
from .views import leave_type_section

admin.site.register(Admin)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(LeaveType)

