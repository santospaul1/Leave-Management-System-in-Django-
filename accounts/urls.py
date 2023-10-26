from django.urls import path
from . import views
app_name = 'accounts'

urlpatterns = [
    path('employee_login/', views.employee_login, name='employee_login'),
    path('recover_password/', views.recover_password, name='recover_password'),

    # Add a URL pattern for changing the password
    # You can specify the empid as an argument to the URL

    # Add other URL patterns as needed
]
