from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from accounts.models import Employee, PasswordRecoveryForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.db.models import Q
def employee_login(request):

    error = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Try to authenticate using empcode or email as the username
        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is None:
            # Create a Q object to perform an OR condition in the query
            q_object = Q(empcode=username) | Q(user__email=username)

            try:
                # Try to get the user based on the OR condition
                employee = Employee.objects.get(q_object)
                user = authenticate(request, username=employee.user.username, password=password)
            except Employee.DoesNotExist:
                user = None

        if user is not None:
            if user.is_active:
                if user.employee.status == 'Active':
                    login(request, user)
                    return redirect('employee_panel:apply_leave')
                else:
                    error = 'Your account is inactive. Please contact the administrator for assistance.'
            else:
                error = 'Your account is inactive. Please contact the administrator for assistance.'
        else:
            error = 'Invalid username or password.'

    return render(request, 'accounts/employee_login.html', {'error': error})

def recover_password(request):
    if request.method == 'POST':
        form = PasswordRecoveryForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            empcode = form.cleaned_data['empcode']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            if new_password == confirm_password:
                try:
                    employee = Employee.objects.get(email=email, empcode=empcode)
                    user = employee.user
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, "Your password has been recovered/changed. Enter new credentials to continue.")
                    return redirect('employee_login')
                except Employee.DoesNotExist:
                    messages.error(request, "Sorry, invalid details.")
            else:
                messages.error(request, "New Password and Confirm Password do not match.")
        else:
            messages.error(request, "Form is invalid.")
    else:
        form = PasswordRecoveryForm()

    return render(request, 'accounts/recover_password.html', {'form': form})


