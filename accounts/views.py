from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

from accounts.models import Employee


# Import your Employee model or adjust the import as needed

def employee_login(request):
    error = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Try to authenticate using empcode as the username
        user = authenticate(request, username=username, password=password)

        # If authentication with empcode failed, try with email
        if user is None:
            try:
                user = User.objects.get(email=username)
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('employee_panel:apply_leave')
            else:
                error = 'Your account is inactive.'
        else:
            error = 'Invalid username or password.'

    return render(request, 'accounts/employee_login.html', {'error': error})

def recover_password(request):
    empid = request.session.get('empid', None)

    if request.method == 'POST':
        if 'submit' in request.POST:
            email = request.POST.get('emailid')
            empid = request.POST.get('empid')

            try:
                employee = Employee.objects.get(EmailId=email, EmpId=empid)
                request.session['empid'] = employee.id
                return render(request, 'change_password.html')
            except Employee.DoesNotExist:
                messages.error(request, "Sorry, Invalid Details.")

        elif 'change' in request.POST:
            new_password = request.POST.get('newpassword')

            if empid:
                try:
                    employee = Employee.objects.get(id=empid)
                    employee.Password = make_password(new_password)
                    employee.save()
                    messages.success(request, "Your password has been recovered. Enter new credentials to continue.")
                    return redirect('employee_login')  # Redirect to the login page or any other URL
                except Employee.DoesNotExist:
                    messages.error(request, "Employee not found.")
            else:
                messages.error(request, "Invalid request.")

    return render(request, 'accounts/recover_password.html')
