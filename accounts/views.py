from django.contrib import messages, auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, RedirectView
from accounts.forms import *
from accounts.models import User
from django.conf import settings
import boto3


class RegisterCustomerView(CreateView):
    model = User
    form_class = CustomerRegistrationForm
    template_name = 'accounts/customer/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        # print(form)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('accounts:login')
        else:
            print(form.errors)
            return render(request, 'accounts/customer/register.html', {'form': form})


class RegisterservicemanView(CreateView):
    """
       Provides the ability to register as a Constant.
    """
    model = User
    form_class = servicemanRegistrationForm
    template_name = 'accounts/serviceman/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            user_email = request.POST.get('email', '')
            ####################################################################################################
            # email_sub = SNS.subscribe("email", user_email)
            SNS = boto3.client('sns',region_name='us-east-1')
            # response = SNS.subscribe(TopicArn='arn:aws:sns:us-east-1:034094653688:scp-service-topic',Protocol='email',Endpoint=user_email)
            response = SNS.subscribe(TopicArn='arn:aws:sns:us-east-1:907329705668:SCP-IHS-topic',Protocol='email',Endpoint=user_email)
            if 'SubscriptionArn' in response:
                print("Successfully subscribed to SNS topic!")
            else:
                print("Failed to subscribe to SNS topic.")

            ####################################################################################################
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/serviceman/register.html', {'form': form})


class LoginView(FormView):
    """
        Provides the ability to login as a user with an email and password
    """
    success_url = '/'
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    extra_context = {
        'title': 'Login'
    }

    def get_success_url(self):
        print("Get-Success-URL method is called")
        if 'next' in self.request.GET and self.request.GET['next'] != '':
            print("IF")
            return self.request.GET['next']
        else:
            print("else")
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def dispatch(self, request, *args, **kwargs):
        print(self.request.user)
        print(self.request.user.is_authenticated)
        print(self.request.user)
        if self.request.user.is_authenticated:
            if self.request.user is not None:
                if self.request.user.is_active:
                    print("You're successfully logged in!")
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        print("Form is Valid")
        auth.login(self.request, form.get_user())
        print("Authentication is successful ")
        print(form.get_user())
        if self.request.user is not None:
            if self.request.user.is_active:
                print("You're successfully logged in!")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    """
        Provides users the ability to logout
    """
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)