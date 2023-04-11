from django.db import models
from django.urls import reverse
from django.utils import timezone

from accounts.managers import UserManager
from accounts.models import User

# department = (
#     ('Primary Education', "Primary Education"),
#     ('Secondary Education', "Secondary Education"),
#     ('Undergraduate Degree', "Undergraduate Degree"),
#     ('Undergraduate Diploma Degree', 'Undergraduate Diploma Degree'),
#     ('Postgraduate Degree', 'Postgraduate Degree'),
#     ('Postgraduate Diploma Degree', 'Postgraduate Diploma Degree'),
#     ('Business Degree', 'Business Degree'),
#     ('Abroad Education', 'Abroad Education'),
# )

department = (
    ('Electrical Service', "Electrical Service"),
    ('Cleaning Service', "Cleaning Service"),
    ('Plumbing Service', "Plumbing Service"),
    ('Air Condition Maintanance', 'Air Condition Maintanance'),
    ('Home Application Maintanance', 'Home Application Maintanance'),
    ('Automobile Service', 'Automobile Service'),
    ('Pet Grooming Service', 'Pet Grooming Service'),
    ('Packers And Movers Service', 'Packers And Movers Service'),
)


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)
    consultation_fees = models.CharField(max_length=100)
    department = models.CharField(choices=department, max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name

    # def get_absolute_url(self):
    # return reverse('appointment:delete-appointment', kwargs={'pk': self.pk})


class TakeAppointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_category = models.CharField(choices=department, max_length=100)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    message = models.TextField()
    phone_number = models.CharField(max_length=120)
    date_time = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    bucket_name = models.CharField(max_length=45)
    obj_key = models.CharField(max_length=150)
    

    def __str__(self):
        return self.full_name

    objects = UserManager()
