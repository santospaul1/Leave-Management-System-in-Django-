from datetime import datetime

from django.http import Http404
from django.shortcuts import render
# Create your views here.
# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from employee_panel.forms import LeaveForm, ProfileUpdateForm
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

    return render(request, 'accounts/change_password.html')

@login_required
def leave_history(request):
    user = request.user
    leave_history = Leave.objects.filter(employee=user.id)

    context = {
        'leave_history': leave_history
    }

    return render(request, 'employee/leave_history.html', context)


def apply_leave(request):
    error = ''
    msg = ''

    leave_types = LeaveType.objects.all()

    if request.method == "POST":
        form = LeaveForm(request.POST)

        if form.is_valid():
            empid = request.user.id
            leavetype = form.cleaned_data['leavetype']
            fromdate = form.cleaned_data['fromdate']
            todate = form.cleaned_data['todate']
            description = form.cleaned_data['description']

            # Calculate date difference
            date_difference = (todate - fromdate).days

            if date_difference < 0:
                error = "End Date should be after Starting Date"
            else:
                leave_type, _ = LeaveType.objects.get_or_create(LeaveType=leavetype, Description=description)
                employee, _ = Employee.objects.get_or_create(empcode=empid)

                leave = Leave.objects.create(
                    employee=employee,
                    leave_type=leave_type,
                    fromdate=fromdate,
                    todate=todate,
                    description=description,
                    status=0,
                    isread=0
                )
                leave.save()
                msg = "Your leave application has been applied. Thank you."
        else:
            error = "Please correct the form errors."
    else:
        form = LeaveForm()

    context = {
        'form': form,
        'leave_types': leave_types,
        'error': error,
        'msg': msg
    }

    return render(request, 'employee/apply_leave.html', context)
@login_required()
def logout(request):
    # Clear session data
    request.session.flush()
    return redirect('accounts:employee_login')  # Redirect to the 'index' URL name or any other URL
@login_required()
def update_profile(request):
    try:
        user_profile = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        # Handle the case where the Employee object does not exist for the user
        raise Http404("Employee profile not found")

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user_profile)
        if form.is_valid():
            employee = form.save()
            messages.success(request, 'Your record has been updated successfully')
        else:
            messages.error(request, 'Form is not valid')
    else:
        form = ProfileUpdateForm(instance=user_profile)

    return render(request, 'employee/update_profile.html', {'form': form})
