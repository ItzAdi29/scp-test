from django import forms
from .models import Appointment, TakeAppointment


class CreateAppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].label = "Full Name"
        self.fields['department'].label = "Select Category you belongs to"
        self.fields['start_time'].label = "Start Time"
        self.fields['consultation_fees'].label = "serviceman Fees"
        self.fields['location'].label = "Office Address"

        self.fields['full_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Full Name',
            }
        )

        self.fields['department'].widget.attrs.update(
            {
                'placeholder': 'Select Your Service',
            }
        )

        self.fields['start_time'].widget.attrs.update(
            {
                'placeholder': 'Ex : 9 AM',
            }
        )
        self.fields['end_time'].widget.attrs.update(
            {
                'placeholder': 'Ex: 5 PM',
            }
        )
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': 'Ex : Dublin, Ireland',
            }
        )

        self.fields['consultation_fees'].widget.attrs.update(
            {
                'placeholder': 'Ex : 75 EUR/Hour',
            }
        )

    class Meta:
        model = Appointment
        fields = ['full_name', 'department', 'start_time', 'end_time', 'location',
                  'consultation_fees']

    def is_valid(self):
        valid = super(CreateAppointmentForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        appointment = super(CreateAppointmentForm, self).save(commit=False)
        if commit:
            appointment.save()
        return appointment


class TakeAppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TakeAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['course_category'].label = "Choose Course Category"
        self.fields['full_name'].label = "Full Name"
        self.fields['phone_number'].label = "Phone Number"
        self.fields['date_time'].label = "Enter Appointment Date"
        self.fields['message'].label = "Message"

        self.fields['course_category'].widget.attrs.update(
            {
                'placeholder': 'Choose Course Category',
            }
        )

        self.fields['full_name'].widget.attrs.update(
            {
                'placeholder': 'Write Your Name',
            }
        )

        self.fields['phone_number'].widget.attrs.update(
            {
                'placeholder': 'Enter Phone Number',
            }
        )
        self.fields['date_time'].widget.attrs.update(
            {
                'placeholder': 'Ex : 24/11/2022',
            }
        )
        self.fields['message'].widget.attrs.update(
            {
                'placeholder': 'Write a short message',
            }
        )

    class Meta:
        model = TakeAppointment
        fields = ['course_category', 'full_name', 'phone_number', 'date_time', 'message']

    def is_valid(self):
        valid = super(TakeAppointmentForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        appointment = super(TakeAppointmentForm, self).save(commit=False)
        if commit:
            appointment.save()
        return appointment


class CustomerAppointmentUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerAppointmentUpdateForm, self).__init__(*args, **kwargs)
        print(self.fields['course_category'])
        self.fields['course_category'].widget.attrs.update()
        self.fields['full_name'].widget.attrs.update()
        self.fields['phone_number'].widget.attrs.update()
        self.fields['date_time'].widget.attrs.update()
        self.fields['message'].widget.attrs.update()

    class Meta:
        model = TakeAppointment
        # fields = ['course_category', 'full_name', 'phone_number', 'date_time', 'message']
        fields = ['course_category', 'full_name', 'phone_number', 'date_time', 'message', 'bucket_name', 'obj_key']

    def is_valid(self):
        valid = super(CustomerAppointmentUpdateForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        appointment = super(CustomerAppointmentUpdateForm, self).save(commit=False)
        if commit:
            appointment.save()
        return appointment