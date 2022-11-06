from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
# Create your views here.



def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			phone_number = form.cleaned_data['phone_number']
			username = email.split('@')[0]
			user = Account.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, phone_number=phone_number, username=username)
			user.phone_number = phone_number
			user.save()
			messages.success(request, 'Registration Successfull. Login to Continue.')
			return redirect('accounts:log_in')
	else:
		form = RegistrationForm()

		
	context = {
		'form':form
	}
	return render(request, 'accounts/register.html', context)


def log_in(request):
	return render(request, 'accounts/login.html')


def log_out(request):
	return render(request, 'accounts/logout.html')