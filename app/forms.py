from .models import Student
from django import forms
from django.forms import DateInput



class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['is_deleted']
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
            'date': DateInput(attrs={'type': 'date'}),
        }



from django import forms
from django.forms.widgets import SelectDateWidget
from .models import Student

class AttendanceForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    attendance_status = forms.ChoiceField(
        choices=[
            ('present', 'Present'),
            ('absent', 'Absent')
        ],
        widget=forms.RadioSelect
    )
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.filter(is_deleted=False),
        widget=forms.CheckboxSelectMultiple,
        required=False  # Allow not selecting any student
    )
    select_all_students = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'select-all-checkbox'})
    )
