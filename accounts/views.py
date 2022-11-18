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

from cart.views import _cart_id
from cart.models import Cart, CartItem
import requests
# Create your views here.


def register(request):

	if request.user.is_authenticated == False:
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
	else:
		messages.success(request, 'You are already logged in.')
		return redirect('accounts:dashboard')

		
	context = {
		'form':form
	}
	return render(request, 'accounts/register.html', context)


def log_in(request):

	if request.user.is_authenticated:

		messages.success(request, 'You are already logged in.')
		return redirect('accounts:dashboard')
	
	else:	

		if request.method == 'POST':		
			email = request.POST['email']
			password = request.POST['password']

			user = auth.authenticate(email=email, password=password)

			if user is not None:

				try:
					cart = Cart.objects.get(cart_id=_cart_id(request))
					is_cart_item_exist = CartItem.objects.filter(cart=cart).exists()

					if is_cart_item_exist:

						cart_item = CartItem.objects.filter(cart=cart)

						# Adding Product Variations by Cart Id from Guest user.
						product_variations = [] #[['blue', 'medium'],['blue', 'medium'],['blue', 'medium']] 
						product_quaintity = []
						for item in cart_item:
							variation = item.product_variation.all()
							product_variations.append(list(variation))
							quantity = item.quality
							product_quaintity.append(quantity)


						# Adding Product Variations from Authenticated user
						cart_item = CartItem.objects.filter(user=user)
						ex_variation_list = [] #[['blue', 'medium'], ['Red', 'medium']]
						cart_item_id = []
						count = 0 #for getting product quantity

						for item in cart_item:
							ex_variation = item.product_variation.all()
							ex_variation_list.append(list(ex_variation))
							cart_item_id.append(item.id)

				
						for pr in product_variations:
							count += 1
							if pr in ex_variation_list:
								index = ex_variation_list.index(pr)
								item_id = cart_item_id[index]
								item_quantity = product_quaintity[count -1]
								item = CartItem.objects.get(id=item_id)
								item.quality += item_quantity
								item.user = user
								item.save()

							else:
								cart_items = CartItem.objects.filter(cart=cart)
								for item in cart_items:
									variation = list(item.product_variation.all())
									if variation not in ex_variation_list:
										item.user = user
										item.save()

				except:
					pass

				auth.login(request, user)
				messages.success(request, 'You are now logged in.')
				url = request.META.get('HTTP_REFERER')  # http://127.0.0.1:8000/accounts/log_in/?next=/cart/checkout/
				try:
					query = requests.utils.urlparse(url).query  # next=/cart/checkout/
					params =dict(x.split('=') for x in query.split('&')) # {'next': '/cart/checkout/'}
					if 'next' in params:
						next_page = params['next']
						return redirect(next_page)
				except:
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



def reset_password(request):

	if request.method == 'POST':
		email = request.POST['email']

		if Account.objects.filter(email__exact=email).exists():
			user = Account.objects.get(email__exact=email)
			current_site = get_current_site(request)
			to_mail = email
			mail_subject = 'Reset your password.'
			mail_messages = render_to_string('accounts/reset_password_email.html', {

			'user':user,
			'domain':current_site,
			'uid':urlsafe_base64_encode(force_bytes(user.pk)),
			'token':default_token_generator.make_token(user),

			})	

			send_mail = EmailMessage(mail_subject, mail_messages, to=[to_mail])
			send_mail.fail_silently = False
			send_mail.send()
			messages.success(request, 'Password reset email has been send to your email address.')
			return redirect('accounts:log_in')
		else:
			messages.error(request, 'Account does not exist!')
			return redirect('accounts:reset_password')

	return render(request, 'accounts/password_reset.html')



def reset_password_validate(request, uidb64, token):

	try:
		uid = urlsafe_base64_decode(uidb64).decode()
		user = Account._default_manager.get(pk=uid)

	except(ValueError, TypeError, OverflowError, Account.DoesNotExist):
		user = None


	if user is not None and default_token_generator.check_token(user, token):
			
		request.session['uid'] = uid
		messages.success(request, 'Please reset your password.')
		return redirect('accounts:reset_password_process')

	else:
		messages.error(request, 'This link has been expired!')
		return redirect('accounts:log_in')





def reset_password_process(request):

	if request.method == 'POST':
		password = request.POST['password']
		confirm_password = request.POST['confirm_password']
		if password == confirm_password:
			uid = request.session.get('uid')
			user = Account.objects.get(pk=uid)
			user.set_password(password)
			user.save()
			messages.success(request, 'Your password has been updated.')
			return redirect('accounts:log_in')
			print(uid, user.pk)
		else:
			messages.error(request, 'Password does not match.')
			return redirect('accounts:reset_password')
	return render(request, 'accounts/reset_password_process.html')