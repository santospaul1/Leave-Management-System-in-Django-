from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from accounts.models import Employee
from django.contrib import messages
from django.contrib.auth import authenticate, login
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
                if employee.status == 'Active':
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
        if 'submit' in request.POST:
            email = request.POST.get('email')
            empcode = request.POST.get('empcode')

            try:
                employee = Employee.objects.get(email=email, empcode=empcode)
                request.session['empid'] = employee.empcode
                return render(request, 'accounts/../myadmin/templates/employee/change_password.html')
            except Employee.DoesNotExist:
                messages.error(request, "Sorry, invalid details.")

        elif 'change' in request.POST:
            new_password = request.POST.get('newpassword')
            empid = request.session.get('empid', None)

            if empid:
                try:
                    employee = Employee.objects.get(id=empid)
                    employee.password = make_password(new_password)
                    employee.save()
                    messages.success(request, "Your password has been recovered. Enter new credentials to continue.")
                    return redirect('employee_login')  # Redirect to the login page or any other URL
                except Employee.DoesNotExist:
                    messages.error(request, "Employee not found.")
            else:
                messages.error(request, "Invalid request.")

    return render(request, 'accounts/recover_password.html')