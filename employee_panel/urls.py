# urls.py

from django.urls import path

from . import views
from .views import change_password, leave_history, apply_leave

urlpatterns = [
    path('change_password/', change_password, name='change_password'),
    path('leave_history/', leave_history, name='leave_history'),
    path('apply_leave/', apply_leave, name='apply_leave'),
    path('logout/', views.logout, name='logout'),
    # Add other URL patterns as needed
]
