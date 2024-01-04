from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .models import Student
from .forms import StudentForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import render, redirect
from .forms import AttendanceForm
from .models import Attendance, Student
from django.contrib import messages
from django.shortcuts import render
from django.db.models import F
from django.db.models import Max
from django.db.models.functions import TruncMonth
from .models import Attendance, Student
from django.utils import timezone
from django.core.mail import send_mail
from django.shortcuts import render
from django.db.models import Count, F, ExpressionWrapper, FloatField
from .models import Attendance, Student



# Create your views here.

def home(request):
    return render(request, 'students/home.html')


def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']

        user=User.objects.create_user(username=username,email=email,password=password)
        user.save()

        return redirect('students:home')

    return render(request,'students/register.html')

def login_user(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['pwd']

        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('students:student_list')
        else:
            return render(request,'students/login.html')

    return render(request,'students/login.html')

def logout_user(request):
    logout(request)
    return render(request, 'students/home.html')


def student_create(request):
    if request.method=="POST":
        form=StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("students:student_list"))
    else:
        form=StudentForm()
    return render(request,"students/student_form.html",{'form':form,})

#list


def student_list(request):
    students = Student.objects.filter(is_deleted=False)  # Exclude deleted students
    return render(request, "students/student_list.html", {"students": students})


# update single task
def student_update(request,pk):
    student = Student.objects.get(pk=pk)
    if request.method == 'POST':
        form=StudentForm(instance=student,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("students:student_detail",args=[pk,]))
    else:
        form=StudentForm(instance=student)

    return render(request,"students/student_form.html",{"form":form, "object":student})

# detail view
def student_detail(request,pk):
    student=Student.objects.get(pk=pk)
    return render(request,"students/student_detail.html",{"student":student,})


#delete

def student_delete(request, pk):
    student_obj = get_object_or_404(Student, pk=pk)
    student_obj.is_deleted = True
    student_obj.save()
    return redirect("students:student_list")



def mark_attendance(request):
    students = Student.objects.filter(is_deleted=False)

    def update_or_create_attendance_record(student, date, status):
        # Check if an attendance record already exists for the student and date
        attendance_record, created = Attendance.objects.get_or_create(
            student=student,
            date=date,
            defaults={'status': status}
        )
        if not created:
            # If the record already exists, update the status
            attendance_record.status = status
            attendance_record.save()

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            attendance_status = form.cleaned_data['attendance_status']
            selected_students = form.cleaned_data['students']
            select_all_students = form.cleaned_data['select_all_students']

            if select_all_students:
                # Update the status for all students
                for student in students:
                    update_or_create_attendance_record(student, date, attendance_status)
            else:
                # Update the status for selected students
                for student in selected_students:
                    update_or_create_attendance_record(student, date, attendance_status)

            return redirect('students:view_attendance')
    else:
        form = AttendanceForm()

    return render(request, 'students/mark_attendance.html', {'form': form, 'students': students})

def deleted_students(request):
    deleted_students = Student.objects.filter(is_deleted=True)
    return render(request, "students/deleted_students.html", {"deleted_students": deleted_students})

# views.py


def student_attendance(request):
    students = Student.objects.filter(is_deleted=False)

    if request.method == 'POST':
        student_id = request.POST.get('student')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        attendance = Attendance.objects.filter(
            student_id=student_id,
            date__range=[from_date, to_date]
        ).order_by('date')

        # Calculate attendance percentages
        total_days = attendance.count()
        present_days = attendance.filter(status='present').count()

        overall_percentage = None

        if total_days > 0:
            overall_percentage = round(present_days / total_days * 100, 2)


        alert_message = None
        if total_days >=6 and overall_percentage is not None and overall_percentage < 75:
            student = Student.objects.get(id=student_id)
            alert_message = 'Shortage of attendance. Percentage is below 75%.'
            subject = 'Attendance Alert'
            message = f'Dear Parent,\n\nAttendance percentage  of  {student.name} having roll number - {student.roll_number} is {overall_percentage}%.\nPlease take necessary actions.'
            from_email = 'kiranhs8577@gmail.com'
            email = student.email
            send_mail(subject, message, from_email, [email])


        return render(request, 'students/student_attendance.html', {'students': students, 'attendance': attendance, 'overall_percentage': overall_percentage, 'alert_message': alert_message})

    return render(request, 'students/student_attendance.html', {'students':students})


def view_attendance(request):
    # Get unique months for which there is attendance data
    unique_months = Attendance.objects.dates('date', 'month', order='DESC')

    # Default to the current month if no month is selected
    selected_month_str = request.GET.get('month', None)

    if selected_month_str:
        selected_month = timezone.datetime.strptime(selected_month_str, "%Y-%m")
    else:
        selected_month = timezone.now()

    # Get all students
    students = Student.objects.filter(is_deleted=False)

    # For each student, get their attendance data for the selected month
    for student in students:
        student.attendance_data = Attendance.objects.filter(
            student=student,
            date__month=selected_month.month,
            date__year=selected_month.year
        ).order_by('date')

    return render(request, 'students/view_attendance.html', {'students': students, 'unique_months': unique_months, 'selected_month': selected_month})


