import hashlib

from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404

from myadmin.models import Leave, Employee
import myadmin
from . import admin
from django.contrib import messages
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

    return render(request, 'admin/add_admin.html')  # Updated template path


def add_department(request):
    if request.method == 'POST':
        department_name = request.POST.get('departmentname')
        department_shortname = request.POST.get('departmentshortname')
        department_code = request.POST.get('deptcode')

        department = Department(DepartmentName=department_name, DepartmentShortName=department_shortname,
                                DepartmentCode=department_code)
        department.save()

        return render(request, 'admin/department_success.html', {'message': 'Department created successfully'})

    return render(request, 'admin/add_department.html')





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
            return render(request, 'admin/employee_success.html')

    else:
        form = EmployeeForm()  # Render an empty form

    return render(request, 'admin/add_employee.html', {'form': form})


def add_leave_type(request):
    if request.method == 'POST':
        leavetype = request.POST['leavetype']
        description = request.POST['description']

        leavetype = LeaveType(LeaveType=leavetype, Description=description)
        leavetype.save()

        # Redirect to a success page or handle success as needed
        return render(request, 'admin/leave_type_success.html')

    else:
        form = LeaveTypeForm()  # Render an empty form

    return render(request, 'admin/add_leave_type.html', {'form': form})


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
    return render(request, 'admin/approved_leaves.html', context)


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


def declined_leaves(request):
    # Add your data retrieval logic here
    # For example, fetching declined leaves and related employee information
    # Replace this with your actual data retrieval logic

    try:
        # Assuming you have Leave and Employee models, you can fetch the data like this
        declined_leaves = Leave.objects.filter(Status=2).order_by('-id')

        # Assuming you have an Employee model with related fields like FirstName and LastName
        results = [{'EmpId': leave.emp.EmpId,
                    'FirstName': leave.emp.FirstName,
                    'LastName': leave.emp.LastName,
                    'LeaveType': leave.LeaveType,
                    'PostingDate': leave.PostingDate,
                    'Status': leave.Status,
                    'lid': leave.id} for leave in declined_leaves]

    except Exception as e:
        error = str(e)
        results = []

    context = {
        'error': error if 'error' in locals() else None,
        'msg': None,  # You can provide a success message if needed
        'results': results,
        'cnt': len(results),
    }

    return render(request, 'admin/declined_leaves.html', context)
def department(request):
    if not request.session.get('alogin'):
        return redirect('index')  # Redirect to the index page if the user is not logged in

    error, msg = None, None

    if 'del' in request.GET:
        department_id = request.GET['del']
        try:
            department = Department.objects.get(id=department_id)
            department.delete()
            msg = "The selected department has been deleted."
        except Department.DoesNotExist:
            error = "The department does not exist."

    departments = Department.objects.all()

    context = {
        'error': error,
        'msg': msg,
        'departments': departments,
    }

    return render(request, 'admin/department.html', context)
def update_department(request, deptid):
    global department
    if not request.session.get('alogin'):
        return redirect('index')  # Redirect to the login page if not logged in

    error = None
    msg = None

    if request.method == 'POST':
        deptname = request.POST.get('departmentname')
        deptshortname = request.POST.get('departmentshortname')
        deptcode = request.POST.get('deptcode')

        try:
            department = Department.objects.get(id=deptid)
            department.DepartmentName = deptname
            department.DepartmentShortName = deptshortname
            department.DepartmentCode = deptcode
            department.save()
            msg = "Department updated successfully"
        except Department.DoesNotExist:
            error = "Department not found or already deleted"

    try:
        department = Department.objects.get(id=deptid)
    except Department.DoesNotExist:
        error = "Department not found"

    context = {
        'error': error,
        'msg': msg,
        'department': department,
    }

    return render(request, 'admin/update_department.html', context)
def update_leave_type(request, lid):
    if not request.session.get('alogin'):
        return redirect('index')  # Redirect to the appropriate URL

    if request.method == 'POST':
        form = LeaveTypeForm(request.POST)
        if form.is_valid():
            leave_type = LeaveType.objects.get(pk=lid)
            leave_type.LeaveType = form.cleaned_data['leavetype']
            leave_type.Description = form.cleaned_data['description']
            leave_type.save()

            msg = "Leave type updated successfully"

    else:
        leave_type = LeaveType.objects.get(pk=lid)
        form = LeaveTypeForm(initial={
            'leavetype': leave_type.LeaveType,
            'description': leave_type.Description
        })

    context = {
        'form': form,
        'msg': msg if 'msg' in locals() else None
    }

    return render(request, 'admin/update_leave_type.html', context)

def employees(request):
    if not request.session.get('alogin'):
        return redirect('index')  # Redirect to the appropriate URL

    msg = None

    if request.method == 'GET':
        if 'inid' in request.GET:
            id = request.GET.get('inid')
            status = 0
            employee = Employee.objects.get(id=id)
            employee.Status = status
            employee.save()
            return redirect('employees')

        if 'id' in request.GET:
            id = request.GET.get('id')
            status = 1
            employee = Employee.objects.get(id=id)
            employee.Status = status
            employee.save()
            return redirect('employees')

    employees = Employee.objects.all()

    context = {
        'employees': employees,
        'msg': msg
    }

    return render(request, 'admin/employees.html', context)
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            admin = Admin.objects.get(UserName=username, Password=password)
            request.session['alogin'] = username
            return redirect('dashboard')  # Redirect to the appropriate URL
        except Admin.DoesNotExist:
            messages.error(request, 'Invalid Details')

    return render(request, 'admin/admin_login.html')


def leaves_history(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')  # Redirect to the login page if not authenticated

    leave_history = Leave.objects.select_related('employee').order_by('-id')  # Assuming you have a Leave model
    return render(request, 'leaves/leave_history.html', {'leave_history': leave_history})


def leave_type_section(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')  # Redirect to the login page if not authenticated

    if request.method == 'GET' and 'del' in request.GET:
        leave_type_id = request.GET['del']
        try:
            leave_type = LeaveType.objects.get(id=leave_type_id)
            leave_type.delete()
            messages.success(request, 'Leave type record deleted')
        except LeaveType.DoesNotExist:
            messages.error(request, 'Leave type record not found')

    leave_types = LeaveType.objects.all()

    return render(request, 'admin/leave_type_section.html', {'leave_types': leave_types})
def user_logout(request):
    logout(request)
    return redirect('index')
def manage_admin(request):
    if not request.user.is_authenticated:
        return redirect('index')  # Redirect to the login page if not authenticated

    if request.method == "GET" and 'del' in request.GET:
        id = request.GET.get('del')
        try:
            admin = Admin.objects.get(id=id)
            admin.delete()
            messages.success(request, "The selected admin account has been deleted")
        except Admin.DoesNotExist:
            messages.error(request, "Admin account not found")

    admins = Admin.objects.all()
    return render(request, 'admin/manage_admin.html', {'admins': admins})