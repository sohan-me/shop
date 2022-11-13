from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.conf import settings
from django.contrib import messages, auth

#Django Verification module
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


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
			user.phone_number = phone_number # For update phone number
			user.save()

			#Accounts Email verification_Function

			current_site = get_current_site(request)
			to_mail = email
			mail_subject = 'Please active your account'
			mail_messages = render_to_string('accounts/accounts_verification_email.html', {

			'user':user,
			'domain':current_site,
			'uid':urlsafe_base64_encode(force_bytes(user.pk)),
			'token':default_token_generator.make_token(user),

			})
			
			email_send = EmailMessage(mail_subject, mail_messages, settings.EMAIL_HOST_USER, to=[to_mail])
			email_send.fail_silently = False
			email_send.send()

			return redirect('/accounts/log_in/?command=verification&email='+email)
	else:
		form = RegistrationForm()

		
	context = {
		'form':form
	}
	return render(request, 'accounts/register.html', context)


def log_in(request):

	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']

		user = auth.authenticate(email=email, password=password)
		if user is not None:
			auth.login(request, user)
			messages.success(request, 'You are now logged in.')
			return redirect('accounts:dashboard')
		else:
			messages.error(request, 'Invalid Email or Password.')
			return redirect('accounts:log_in')

	return render(request, 'accounts/login.html')


def log_out(request):
	if request.user.is_authenticated:
		auth.logout(request)
		messages.success(request, 'You are now logged out.')
	else:
		messages.success(request, 'You are already logged out.')
		return redirect('accounts:log_in')
	return redirect('accounts:log_in')




def activate(request, uidb64, token):
	
	try:
		uid = urlsafe_base64_decode(uidb64).decode()
		user = Account._default_manager.get(pk=uid)
	except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
		user = None

	if user is not None and default_token_generator.check_token(user, token):
		user.is_active = True
		user.save()
		messages.success(request, 'Congratulations! Your account is activated.')
		return redirect('accounts:log_in')

	else:
		messages.error(request, 'Invalid activation link.')
		return redirect('accounts:register')



def dashboard(request):
	return render(request, 'accounts/dashboard.html')