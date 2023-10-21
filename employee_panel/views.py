from datetime import datetime

from django.shortcuts import render
# Create your views here.
# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from myadmin.models import Leave, LeaveType, Employee


@login_required
def change_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        new_password = request.POST['newpassword']
        confirm_password = request.POST['confirmpassword']

        user = request.user

        if user.check_password(password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your Password Has Been Updated.')
            else:
                messages.error(request, 'New Password and Confirm Password do not match.')
        else:
            messages.error(request, 'Your current password is wrong.')

    return render(request, 'employee/change_password.html')

@login_required
def leave_history(request):
    user = request.user
    leave_history = Leave.objects.filter(empid=user.id)

    context = {
        'leave_history': leave_history
    }

    return render(request, 'employee/leave_history.html', context)
def apply_leave(request):
    if request.method == "POST":
        empid = request.user.id
        leavetype = request.POST['leavetype']
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']
        description = request.POST['description']

        # Calculate date difference
        from_date = datetime.datetime.strptime(fromdate, '%Y-%m-%d')
        to_date = datetime.datetime.strptime(todate, '%Y-%m-%d')
        date_difference = (to_date - from_date).days

        if date_difference < 0:
            error = "End Date should be after Starting Date."
        else:
            # Create a Leave object
            leave = Leave.objects.create(
                empid=empid,
                LeaveType=leavetype,
                FromDate=fromdate,
                ToDate=todate,
                Description=description,
                Status=0,
                IsRead=0
            )
            leave.save()
            msg = "Your leave application has been applied. Thank you."

    leave_types = LeaveType.objects.all()

    context = {
        'leave_types': leave_types,
        'error': error,
        'msg': msg
    }

    return render(request, 'employee/apply_leave.html', context)
def logout(request):
    # Clear session data
    request.session.flush()
    return redirect('index')  # Redirect to the 'index' URL name or any other URL
def update_profile(request):
    if not request.session.get('emplogin'):
        return redirect('index')  # Redirect to the 'index' URL name or any other URL

    if request.method == 'POST':
        eid = request.session['emplogin']
        try:
            employee = Employee.objects.get(EmailId=eid)
            employee.FirstName = request.POST.get('firstName')
            employee.LastName = request.POST.get('lastName')
            employee.Gender = request.POST.get('gender')
            employee.Dob = request.POST.get('dob')
            employee.Department = request.POST.get('department')
            employee.Address = request.POST.get('address')
            employee.City = request.POST.get('city')
            employee.Country = request.POST.get('country')
            employee.Phonenumber = request.POST.get('mobileno')
            employee.save()
            messages.success(request, 'Your record has been updated successfully')
        except Employee.DoesNotExist:
            messages.error(request, 'Employee not found')

    # Fetch the employee data for pre-filling the form
    eid = request.session.get('emplogin')
    try:
        employee = Employee.objects.get(EmailId=eid)
    except Employee.DoesNotExist:
        employee = None

    return render(request, 'employee/update_profile.html', {'employee': employee})