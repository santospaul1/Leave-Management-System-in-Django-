from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from django.db.models import Q
from myadmin.models import Leave, Employee
import myadmin
from . import admin
from .forms import EmployeeForm, LeaveTypeForm
from .models import Admin, Department, Employee, LeaveType, Leave


def add_admin(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')

        admin = Admin(fullname=fullname, email=email, password=password, username=username)
        admin.save()

        return render(request, 'admin/success.html', {'message': 'New admin has been added successfully'})

    return render(request, 'myadmin/add_admin.html')  # Updated template path


def add_department(request):
    if request.method == 'POST':
        department_name = request.POST.get('departmentname')
        department_shortname = request.POST.get('departmentshortname')
        department_code = request.POST.get('deptcode')

        department = Department(DepartmentName=department_name, DepartmentShortName=department_shortname,
                                DepartmentCode=department_code)
        department.save()

        return render(request, 'myadmin/department_success.html', {'message': 'Department created successfully'})

    return render(request, 'myadmin/add_department.html')





def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            empid = form.cleaned_data['empcode']
            fname = form.cleaned_data['firstName']
            lname = form.cleaned_data['lastName']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            gender = form.cleaned_data['gender']
            dob = form.cleaned_data['dob']
            department = form.cleaned_data['department']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            country = form.cleaned_data['country']
            mobileno = form.cleaned_data['mobileno']
            status = 1  # Assuming status is hardcoded to 1

            employee = Employee(
                empcode=empid,
                firstName=fname,
                lastName=lname,
                email=email,
                password=password,
                gender=gender,
                dob=dob,
                department=department,
                address=address,
                city=city,
                country=country,
                mobileno=mobileno,
                status=status,
            )

            employee.save()  # Save the employee to the database

            # Redirect to a success page or handle success as needed
            return render(request, 'employee_success.html')

    else:
        form = EmployeeForm()  # Render an empty form

    return render(request, 'add_employee.html', {'form': form})


def add_leave_type(request):
    if request.method == 'POST':
        leavetype = request.POST['leavetype']
        description = request.POST['description']

        leavetype = LeaveType(LeaveType=leavetype, Description=description)
        leavetype.save()

        # Redirect to a success page or handle success as needed
        return render(request, 'leave_type_success.html')

    else:
        form = LeaveTypeForm()  # Render an empty form

    return render(request, 'add_leave_type.html', {'form': form})


def approved_leaves(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to your login page
    error = None
    msg = None
    approved_leaves = LeaveType.objects.filter(Status=1)

    if request.method == 'POST':
        # Handle any POST requests if needed
        pass
    leaves = Leave.objects.filter(Status=1).order_by('-id')

    context = {
        'error': error,
        'msg': msg,
        'approved_leaves': approved_leaves,
    }
    return render(request, 'approved_leaves.html', context)


def update_employee(request, empid):
    # Implement this view for updating employee details
    employee = get_object_or_404(LeaveType, id=empid)
    pass
def employee_leave_details(request, leaveid):
    # Implement this view for viewing leave details
    # You can use get_object_or_404 to get the leave by leaveid
    leave = get_object_or_404(LeaveType, id=leaveid)
    # Add any code to display leave details here
    pass
def dashboard(request):
    if not request.session.get('alogin'):
        return redirect('index')  # Redirect to your login page or appropriate URL
    #emp_count = get_employee_count()
    #leave_count = get_leave_count()
    leaves = Leave.objects.order_by('-id')[:7]

    context = {
        'page': 'dashboard',  # Set the current page
        'leaves': leaves,
    }

    return render(request, 'admin/dashboard.html', context)


