from django.db import models


class Student(models.Model):
    name = models.CharField(verbose_name="Student name", max_length=100)
    father_name = models.CharField(verbose_name="father name", max_length=100)
    mother_name = models.CharField(verbose_name="mother name", max_length=100)
    date_of_birth = models.DateField()
    contact_number = models.CharField(verbose_name="contact no", max_length=15)
    date = models.DateField(verbose_name="date of admission")
    class_name = models.CharField(verbose_name="class", max_length=50)
    address = models.TextField()
    email = models.EmailField(verbose_name="parent email", max_length=100)

    # Add a unique roll number field
    roll_number = models.CharField(verbose_name="roll number", max_length=20, unique=True)

    is_deleted = models.BooleanField(default=False)



    def __str__(self):

        return f"{self.name} - {self.roll_number}"



class Attendance(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"


