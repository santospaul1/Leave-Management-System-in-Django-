from django.urls import path
from . import views

app_name = 'myadmin'

urlpatterns = [
    path('add_admin/', views.add_admin, name='add_admin'),
    path('add_department/', views.add_department, name='add_department'),
    path('add_leave_type/', views.add_leave_type, name='add_leave_type'),
    path('approved-leaves/', views.approved_leaves, name='approved_leaves'),
    path('update-employee/<int:empid>/', views.update_employee, name='update_employee'),
    path('employee-leave-details/<int:leaveid>/', views.employee_leave_details, name='employee_leave_details'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Add other URL patterns for your views
]
