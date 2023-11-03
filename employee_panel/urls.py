# urls.py

from django.urls import path

from . import views
from .views import leave_history, apply_leave, change_password

app_name='employee_panel'

urlpatterns = [
    path('change_password/', change_password, name='change_password'),
    path('leave_history/', leave_history, name='leave_history'),
    path('apply_leave/', apply_leave, name='apply_leave'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('logout/', views.logout, name='logout'),

    # Add other URL patterns as needed
]
