from datetime import datetime

from django.db.models import Q
from django.http import Http404

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from employee_panel.forms import LeaveForm, ProfileUpdateForm
from myadmin.models import Leave, LeaveType, Employee, Department


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
    leave_history = Leave.objects.filter(employee=user.id)
    status = Leave.status
    context = {
        'status':status,
        'leave_history': leave_history

    }

    return render(request, 'employee/leave_history.html', context)


@login_required
def apply_leave(request):
    error = ''
    msg = ''

    if request.method == "POST":
        form = LeaveForm(request.POST)

        if form.is_valid():
            user = request.user  # Get the currently logged-in User instance
            leavetype = form.cleaned_data['leavetype']
            fromdate = form.cleaned_data['fromdate']
            todate = form.cleaned_data['todate']
            description = form.cleaned_data['description']

            #employee = Employee.objects.all(empcode=id)
            # Calculate date difference
            date_difference = (todate - fromdate).days


            if date_difference < 0:
                error = "End Date should be after Starting Date"
            else:

                leave = Leave.objects.create(
                    employee=user,
                    leavetype=leavetype,
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
def update_profile(request, empcode):

  employee = get_object_or_404(Employee, empcode=empcode)

  form = ProfileUpdateForm(instance=employee)

  if request.method == 'POST':
    form = ProfileUpdateForm(request.POST, instance=employee)
    if form.is_valid():
      form.save()
      return redirect('employee_panel:apply_leave')

  return render(request, 'employee/update_profile.html', {'form': form, 'employee': employee})
