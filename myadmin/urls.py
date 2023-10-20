from django.urls import path
from . import views
from .views import update_leave_type, employees

app_name = 'myadmin'

urlpatterns = [
    path('add_admin/', views.add_admin, name='add_admin'),
    path('add_department/', views.add_department, name='add_department'),
    path('add_leave_type/', views.add_leave_type, name='add_leave_type'),
    path('approved-leaves/', views.approved_leaves, name='approved_leaves'),
    path('update-employee/<int:empid>/', views.update_employee, name='update_employee'),
    path('employee-leave-details/<int:leaveid>/', views.employee_leave_details, name='employee_leave_details'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('declined-leaves/', views.declined_leaves, name='declined_leaves'),
    path('update_department/<int:deptid>/', views.update_department, name='update_department'),
    path('update_leave_type/<int:lid>/', views.update_leave_type, name='update_leave_type'),
    path('employees/', views.employees, name='employees'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('leaves_history/', views.leaves_history, name='leave_history'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('manage-admin/', views.manage_admin, name='manage_admin'),
    # Add other URL patterns for your views
]
