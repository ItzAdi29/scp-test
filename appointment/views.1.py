from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from accounts.models import User
from .decorators import user_is_customer, user_is_serviceman
from django.views.generic import TemplateView, UpdateView, CreateView, ListView, DetailView, DeleteView
from django.views.generic.edit import DeleteView, UpdateView
from accounts.forms import CustomerProfileUpdateForm, servicemanProfileUpdateForm
from .forms import CreateAppointmentForm, TakeAppointmentForm, CustomerAppointmentUpdateForm
from .models import Appointment, TakeAppointment
from django.conf import settings
from django.core.mail import send_mail
import boto3
import io
import json
import requests
import pandas as pd
import os

"""
For customer Profile
    
"""



class EditCustomerProfileView(UpdateView):
    model = User
    form_class = CustomerProfileUpdateForm
    context_object_name = 'customer'
    template_name = 'accounts/customer/edit-profile.html'
    success_url = reverse_lazy('accounts:customer-profile-update')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_customer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")
        # context = self.get_context_data(object=self.object)
        print(self.get_context_data())
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("customer doesn't exists")
        return obj


"""

"""


# class TakeAppointmentView(CreateView):
#     template_name = 'appointment/take_appointment.html'
#     form_class = TakeAppointmentForm
#     extra_context = {
#         'title': 'Take Appointment'
#     }
#     success_url = reverse_lazy('appointment:home')

#     @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
#     def dispatch(self, request, *args, **kwargs):
#         if not self.request.user.is_authenticated:
#             return reverse_lazy('accounts:login')
#         if self.request.user.is_authenticated and self.request.user.role != 'customer':
#             return reverse_lazy('accounts:login')
#         return super().dispatch(self.request, *args, **kwargs)

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         user_name = form.instance.user
#         return super(TakeAppointmentView, self).form_valid(form)

#     def post(self, request, *args, **kwargs):
#         self.object = None
#         form = self.get_form()
#         if form.is_valid():
#             name = request.POST.get('full_name','')
#             department = request.POST.get('course_category','')
#             phone_number = request.POST.get('phone_number','')
#             date_time = request.POST.get('date_time','')
#             message = request.POST.get('message','')
#             # location = request.POST.get('location','')
            
#             # form.save()
            
#             # self.form_valid(form)
            
#             # url = 'https://jatsuhvmea.execute-api.us-east-1.amazonaws.com/createPDF/create'
#             url = 'https://r6p1p8siqg.execute-api.us-east-1.amazonaws.com/pdfcreate/create'

#             data = {
#                 'Service_Category': department,
#                 'Full_Name': name,
#                 'Phone_Number': phone_number,
#                 'Date': date_time,
#                 'Data': message,
#                 'S3': 'scp-api-test-bucket',
#                 'S3_File': 'Input docx.docx',
#                 'SNS_ARN': 'arn:aws:sns:us-east-1:569186011793:scp-topic'
#             }
            
#                 # 'S3': 'scp-service-man',
#                 # 'SNS_ARN': 'arn:aws:sns:us-east-1:034094653688:scp-service-topic'
            
#             headers = {
#                 'Content-Type': 'application/json'
#             }
            
#             response = requests.post(url, data=json.dumps(data), headers=headers)
            
#             if response.status_code == 200:
#                 json_response = response.json()
#                 # Bucket = json_response['Bucket']
#                 # Key = json_response['Key']
#                 print ("json response - ",json_response)
#                 print('------------')
#                 Bucket = str(json_response['Bucket'])
#                 Key = str(json_response['Key'])
#                 print (Bucket + "    " + Key)
            
                
#                 # mymembers = TakeAppointment.objects.all()
#                 # # print(mymembers)
#                 # # mymembers.delete()
#                 # mymember = mymembers.filter(full_name=name, course_category=department, date_time=date_time).values()
#                 # # mymember = mymembers.filter(full_name=name, course_category=department, date_time=date_time)
#                 # mymember = mymember.update(bucket_name=Bucket, obj_key=Key)
#                 # mymember.save()
                
#                 # mymember = TakeAppointment.objects.filter(full_name=name, course_category=department, date_time=date_time).first()
#                 # if mymember:
#                 #     mymember.bucket_name = Bucket
#                 #     mymember.obj_key = Key
#                 #     mymember.save()
                
#                 mymembers = TakeAppointment.objects.filter(full_name=name, course_category=department, date_time=date_time)
#                 mymembers.update(bucket_name=Bucket, obj_key=Key)


                
                
#                  # Print the row data to the console
#                 # print(my_obj)
#                 # my_obj=TakeAppointment.objects.filter(full_name=name, course_category=department, date_time=date_time, phone_number=phone_number).values().update(bucket_name=Bucket, obj_key=Key)
                
#                 # my_obj = TakeAppointment.objects.get(full_name=name, course_category=department, date_time=date_time, phone_number=phone_number)
#                 # my_obj.bucket_name = Bucket
#                 # my_obj.obj_key = Key
#                 # my_obj.save()
                
#                 # my_obj1=TakeAppointment.objects.filter(full_name=name, course_category=department, date_time=date_time, phone_number=phone_number).values()
#                 # print(my_obj1)
                
#                 # mymembers = TakeAppointment.objects.all()
#                 # mymembers.save()
                
#                 # print(mymembers)
                
#             else:
#                 print('Request failed with status code:', response.status_code)

            
            
#             ####################################################################################################
#             #field_course_category = request.POST.get('course_category','')
#             #field_full_name = request.POST.get('full_name','')
#             #field_date_time = request.POST.get('date_time','')
#             #message = 'An appoinment has been booked for ' + field_course_category + ' by ' + field_full_name + ' on ' + field_date_time + '.'
#             #subject = 'Appointment has been created !!!!!!.'
#             #email_pub=SNS.publish(message, subject)
#             ####################################################################################################
#             # return None
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

class TakeAppointmentView(CreateView):
    template_name = 'appointment/take_appointment.html'
    form_class = TakeAppointmentForm
    extra_context = {
        'title': 'Take Appointment'
    }
    success_url = reverse_lazy('appointment:home')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'customer':
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        user_name = form.instance.user
        return super(TakeAppointmentView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            name = request.POST.get('full_name','')
            department = request.POST.get('course_category','')
            phone_number = request.POST.get('phone_number','')
            date_time = request.POST.get('date_time','')
            message = request.POST.get('message','')
            
            self.form_valid(form)
            
            # url = 'https://jatsuhvmea.execute-api.us-east-1.amazonaws.com/createPDF/create'
            url = 'https://r6p1p8siqg.execute-api.us-east-1.amazonaws.com/pdfcreate/create'

            data = {
                'Service_Category': department,
                'Full_Name': name,
                'Phone_Number': phone_number,
                'Date': date_time,
                'Data': message,
                'S3': 'scp-api-test-bucket',
                'S3_File': 'Input docx.docx',
                'SNS_ARN': 'arn:aws:sns:us-east-1:569186011793:scp-topic'
            }
            
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, data=json.dumps(data), headers=headers)
            
            if response.status_code == 200:
                json_response = response.json()
                Bucket = str(json_response['Bucket'])
                Key = str(json_response['Key'])
                print (Bucket + "    " + Key)
        
                appointment = form.save(commit=False)
                appointment.bucket_name = Bucket
                appointment.obj_key = Key
                appointment.save()
                
            else:
                print('Request failed with status code:', response.status_code)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


"""
   For Service Person Profile
"""


class EditservicemanProfileView(UpdateView):
    model = User
    form_class = servicemanProfileUpdateForm
    context_object_name = 'serviceman'
    template_name = 'accounts/serviceman/edit-profile.html'
    success_url = reverse_lazy('accounts:serviceman-profile-update')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_serviceman)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")
        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("Customer doesn't exists")
        return obj

"""
    Service Person Appointment Create
"""


class AppointmentCreateView(CreateView): 
    template_name = 'appointment/appointment_create.html'
    form_class = CreateAppointmentForm
    extra_context = {
        'title': 'Post New Appointment'
    }
    success_url = reverse_lazy('appointment:serviceman-appointments')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'serviceman':
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AppointmentCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()

        if form.is_valid():
        
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


"""

   Service Persons Appointments

"""


class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointment/appointment.html'
    context_object_name = 'appointment'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_serviceman)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id).order_by('-id')


"""

    Available serviceman/s for Customer
    
"""


class servicemanListView(ListView):
    model = Appointment
    template_name = 'appointment/serviceman_list_by_category.html'
    context_object_name = 'serviceman_list'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_customer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        print(self.request.user.id)
        # Filter the Objects Using User Id.
        # return self.model.objects.filter(user_id=self.request.user.id).order_by('-id')
        # returning all list
        return self.model.objects.all
        

"""

    Customer Appointment History List
    
"""


class CustomerAppointmentHistoryListView(ListView):
    model = TakeAppointment
    context_object_name = 'customer_appointment_history_list'
    template_name = "appointment/customer_appointment_history.html"

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_customer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id).order_by('-id')


class CustomerDeleteAppointmentView(DeleteView):
    model = TakeAppointment
    success_url = reverse_lazy('appointment:customer-appointment-history')


class AppointmentDeleteView(DeleteView):
    """
       For Delete any Appointment created by serviceman
    """
    model = Appointment
    success_url = reverse_lazy('appointment:serviceman-appointments')


class UpdateCustomerAppointmentView(UpdateView):
    model = TakeAppointment
    form_class = CustomerAppointmentUpdateForm
    template_name = 'accounts/customer/update_customer_appointment.html'
    success_url = reverse_lazy('appointment:customer-appointment-history')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_customer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    # 'QuerySet' object has no attribute '_meta'
    # The get_object method returns queryset i.e., list of records, instead of instance. To get instance
    # we can use first() on filter() . This gives you first occurrence.
    def get_object(self, queryset=None, **kwargs):
        # Filter the data using User id and appointment id
        print("Total Objects in Appointment History Table " + str(self.model.objects.all().count()))
        filtered_object = self.model.objects.filter(user_id=self.request.user.id, id=kwargs.get('pk'))
        print("Object count after running the FILTER  " + str(filtered_object.all().count()))
        
        print('---------------------------------filtered_object : ',filtered_object)

        return filtered_object.first()

    def get(self, request, *args, **kwargs):
        try:
            # Calling get_object() method to create Object and assign to Object Variable
            self.object = self.get_object(**kwargs)
        except Http404:
            raise Http404("User doesn't exists")
        # rendering the Template by Passing Context data
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form, **kwargs):
        form.instance.user = self.request.user

        # Delete a record from Table using Django Model (Deleting the Existing Appointment)
        Object_to_be_delete = self.model.objects.filter(user_id=self.request.user.id, id=kwargs.get('pk'))
        print(Object_to_be_delete.delete())
        return super(UpdateCustomerAppointmentView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            name = request.POST.get('full_name','')
            department = request.POST.get('course_category','')
            phone_number = request.POST.get('phone_number','')
            date_time = request.POST.get('date_time','')
            message = request.POST.get('message','')
            # location = request.POST.get('location','')
            print(name, department, phone_number, date_time, message)
            
            self.form_valid(form)
            
            # url = 'https://jatsuhvmea.execute-api.us-east-1.amazonaws.com/createPDF/delete'
            url = 'https://r6p1p8siqg.execute-api.us-east-1.amazonaws.com/pdfcreate/update'


            data = {
                'Service_Category': department,
                'Full_Name': name,
                'Phone_Number': phone_number,
                'Date': date_time,
                'Data': message,
                # 'S3': 'scp-service-man',
                'S3': 'scp-api-test-bucket',
                'key' : 'Some CategoryJohn Doe12345678902023-04-04.pdf',
                'S3_File': 'Input docx.docx',
                # 'SNS_ARN': 'arn:aws:sns:us-east-1:034094653688:scp-service-topic'
                'SNS_ARN': 'arn:aws:sns:us-east-1:569186011793:scp-topic'
            }
            

            headers = {
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, data=json.dumps(data), headers=headers)
            
            if response.status_code == 200:
                json_response = response.json()
                Bucket = json_response['Bucket']
                Key = json_response['Key']
                print (Bucket + "    " + Key)
                
                
                mymembers = TakeAppointment.objects.all()
                # mymembers.delete()
                mymember = mymembers.filter(full_name=name, course_category=department, date_time=date_time).values()
                mymember.update(obj_key=Key)
            
                
            else:
                print('Request failed with status code:', response.status_code)
            
            
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form)


"""
   For both Profile
   
"""


class HomePageView(ListView):
    paginate_by = 9
    model = Appointment
    context_object_name = 'home'
    template_name = "home.html"

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')


class ServiceView(TemplateView):
    template_name = 'appointment/service.html'


class SearchView(ListView):
    paginate_by = 6
    model = Appointment
    template_name = 'appointment/search.html'
    context_object_name = 'appointment'

    def get_queryset(self):
        return self.model.objects.filter(location__contains=self.request.GET['location'],
                                         department__contains=self.request.GET['department'])


def query(request):
   if request.method == "POST":
       print(request)
       name= request.POST.get('name','')
       mail= request.POST.get('mail','')
       contactno = request.POST.get('contactno', '')
       question = request.POST.get('question', '')

    
       url = "https://y7az312pz5.execute-api.us-east-1.amazonaws.com/test"

       payload = {
                  "a": name,
                  "b": mail,
                  "c": contactno,
                  "d": question,
                  "e": "arn:aws:sns:us-east-1:034094653688:scp-topic"
                }

       response = requests.post(url, data=json.dumps(payload))
       print(response.status_code)
       
    #  contactus = Contact(name=name ,mail=mail, contactno=contactno , question=question)
    #  contactus.save()
   return render(request , 'query.html')
   
   
   
def map_location(request):
    s3 = boto3.resource('s3')
    API_KEY = 'JjwheWGTI0y3UKYToQj0HDa58vxc3bj2'
    # Fetch Excel file from S3
    # bucket_name = 'scp-service-man'
    bucket_name = 'scp-api-test-bucket'
    file_name = 'map location.xlsx'
    obj = s3.Object(bucket_name, file_name)
    excel_data = obj.get()['Body'].read()
    
    # Parse Excel file to get location data
    df = pd.read_excel(excel_data)
    locations = []
    for index, row in df.iterrows():
        location = {'name': row['location name'], 'lat': row['latitude'], 'lng': row['longitude']}
        locations.append(location)
    
    # Call MapQuest API to get the map
    markers = "||".join([f"{loc['lat']},{loc['lng']}" for loc in locations])
    url = f"https://www.mapquestapi.com/staticmap/v5/map?key={API_KEY}&size=1920,1080&zoom=10&locations={markers}"
    response = requests.get(url)
    
    # Save map to Media folder and return HTML page
    # media_folder = os.path.join('/in_home_service/static', 'map.png')
    media_folder = os.path.join(settings.BASE_DIR, 'static', 'map.png')
    os.makedirs(os.path.dirname(media_folder), exist_ok=True)
    with open(media_folder, 'wb') as f:
        f.write(response.content)
    # map_url = '/static/map.png'
    # return render(request , 'map.html', {'map_var':map_url})
    return render(request, 'map.html')