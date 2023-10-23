from django.urls import path
from . import views

urlpatterns = [
    path('employee_login/', views.employee_login, name='employee_login'),
    path('recover_password/', views.recover_password, name='recover_password'),

    # Add a URL pattern for changing the password
    # You can specify the empid as an argument to the URL
    path('change_password/', views.change_password, name='change_password'),
    # Add other URL patterns as needed
]
