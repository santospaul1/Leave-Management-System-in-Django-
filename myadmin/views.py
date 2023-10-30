import hashlib
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Notification
from django.contrib import messages
from .forms import EmployeeForm, LeaveTypeForm, EmployeeUpdateForm, AdminForm
from .models import Admin, Department, Employee, LeaveType, Leave

# Rest of your views...



def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('myadmin:dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'admin/admin_login.html')



@login_required
def user_logout(request):
    logout(request)
    return redirect('myadmin:admin_login')
@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    leaves = Leave.objects.order_by('-id')[:7]
    notifications = Notification.objects.filter(user=request.user, is_read=False)[:5]

    context = {
        'page': 'dashboard',
        'leaves': leaves,
        'notifications': notifications,
    }

    return render(request, 'admin/dashboard.html')
@login_required
def add_admin(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')

        admin = Admin(fullname=fullname, email=email, username=username)
        admin.set_password(password)  # Set the password securely
        admin.save()

        return render(request, 'admin/success.html', {'message': 'New admin has been added successfully'})

    return render(request, 'admin/add_admin.html')

@login_required
def add_department(request):
    if request.method == 'POST':
        department_name = request.POST.get('department_name')
        department_shortname = request.POST.get('department_shortname')
        department_code = request.POST.get('department_code')

        department = Department(department_name=department_name, department_shortname=department_shortname,
                                department_code=department_code)
        Department.objects.filter(Q(department_name__isnull=True) | Q(department_shortname__isnull=True)).delete()
        department.save()

        return render(request, 'admin/department_success.html', {'message': 'Department created successfully'})

    return render(request, 'admin/add_department.html')




@login_required
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

@login_required
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
@login_required
def leave_type_list(request):
    leave_types = LeaveType.objects.all()  # Query all leave types
    return render(request, 'admin/leave_type_list.html', {'leave_types': leave_types})
@login_required
def approved_leaves(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to your login page
    error = None
    msg = None
    approved_leaves = Leave.objects.filter(status=1)

    if request.method == 'POST':
        query = Leave.objects.all()

        # Execute the query and get the results
        results = query.values()

        # Get the count of results
        leavtypcount = query.count()
    leaves = Leave.objects.filter(status=1).order_by('-id')

    context = {
        'error': error,
        'msg': msg,
        'approved_leaves': approved_leaves,
    }
    return render(request, 'admin/approved_leaves.html', context)

@login_required
def update_employee(request, empid):
    # Implement this view for updating employee details
    employee = get_object_or_404(LeaveType, id=empid)
    pass
@login_required
def employee_leave_details(request, leaveid):
    # Implement this view for viewing leave details
    # You can use get_object_or_404 to get the leave by leaveid
    leave = get_object_or_404(LeaveType, id=leaveid)
    # Add any code to display leave details here
    pass



@login_required
def declined_leaves(request):
    declined_leaves = Leave.objects.filter(status=2).order_by('-id')
    context = {
        'declined_leaves': declined_leaves
    }
    return render(request, 'admin/declined_leaves.html', context)
@login_required
def department(request):
    if request.method == "GET" and 'del' in request.GET:
        department_id = request.GET['del']
        try:
            department = Department.objects.get(id=department_id)
            department.delete()
            messages.success(request, "Department deleted successfully")
        except Department.DoesNotExist:
            messages.error(request, "Department not found")

    departments = Department.objects.all()
    return render(request, 'admin/department_list.html', {'departments': departments})
@login_required
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
@login_required
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
@login_required
def employees(request):

    if not request.user.is_authenticated:
        return redirect('admin_login')  # Redirect to the appropriate URL

    msg = None

    if request.method == 'GET':
        if 'inid' in request.GET:
            id = request.GET.get('inid')
            status = "Inactive"
            employee = Employee.objects.get(id=id)
            employee.Status = status
            employee.save()
            return redirect('employees')

        if 'id' in request.GET:
            id = request.GET.get('id')
            status = "Active"
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
@login_required
def leaves_history(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')  # Redirect to the login page if not authenticated

    leave_history = Leave.objects.select_related('employee').order_by('-id')  # Assuming you have a Leave model
    return render(request, 'admin/leaves_history.html', {'leave_history': leave_history})

@login_required
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
@login_required
def manage_admin(request):
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
@login_required
def pending_leaves(request):
    leaves = Leave.objects.filter(status=0).order_by('-id')
    context = {
        'leaves': leaves
    }
    return render(request, 'admin/pending_history.html', context)

@login_required
def employee_update(request, id):

  employee = get_object_or_404(Employee, id=id)

  form = EmployeeUpdateForm(instance=employee)

  if request.method == 'POST':
    form = EmployeeUpdateForm(request.POST, instance=employee)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/employees')

  return render(request, 'admin/update.html', {'form': form})



def approved_app_counter_view(request):

    leavtypcount = LeaveType.objects.count()

    context = {
        'leavtypcount': leavtypcount,
    }

    return render(request, 'admin/approvedapp-counter.html', context)


def declined_leaves_counter(request):
    leavetype_count = LeaveType.objects.filter(status='2').count()

    return render(request, 'admin/declineapp-counter.html', {'leavetype_count': leavetype_count})


def count_departments(request):
    department_count = department.objects.count()

    return render(request, 'admin/dept-counter.html', {'department_count': department_count})


def count_employees(request):
    employee_count = employees.objects.count()

    return render(request, 'admin/emp-counter.html', {'employee_count': employee_count})


def count_leave_types(request):
    leave_type_count = LeaveType.objects.count()

    return render(request, 'leavetype-counter.html', {'leave_type_count': leave_type_count})


def count_pending_leaves(request):
    pending_leave_count = LeaveType.objects.filter(Status=0).count()

    return render(request, 'admin/pendingapp-counter.html', {'pending_leave_count': pending_leave_count})