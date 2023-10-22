from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

from myadmin.models import Employee


# Import your Employee model or adjust the import as needed

def employee_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            employee = Employee.objects.get(EmailId=username)
            if check_password(password, employee.Password):
                if not employee.Status:
                    messages.error(request, "In-Active Account. Please contact your administrator!")
                else:
                    request.session['emplogin'] = username
                    return redirect('employee_leave')  # Redirect to the 'employee_leave' URL name or any other URL
            else:
                messages.error(request, "Sorry, Invalid Details.")
        except Employee.DoesNotExist:
            messages.error(request, "Sorry, Invalid Details.")

    return render(request, 'login_employee/employee_login.html')
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

    return render(request, 'login_employee/recover_password.html')


def change_password(request):
    empid = request.GET.get('empid')
    if not empid:
        return render(request, 'invalid_request.html')  # Create an 'invalid_request.html' template for this purpose

    if request.method == 'POST':
        new_password = request.POST['newpassword']
        # Perform the password change logic here and handle any errors
        # If successful, consider redirecting to a success page

    return render(request, 'login_employee/change_password.html', {'empid': empid})
# Add any other necessary imports and view functions

# Add any other necessary imports and view functions
