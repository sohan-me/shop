from django.shortcuts import render, redirect, HttpResponse
from cart.models import CartItem
from .forms import OrderForm
import datetime, json
from .models import Order, Payment, OrderProduct
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse

# Create your views here.




def place_order(request, total=0, quantity=0):

	current_user = request.user
	cart_items = CartItem.objects.filter(user=current_user, is_active=True)
	cart_count = cart_items.count()
	if cart_count <=0:
		return redirect('store:store')

	for cart_item in cart_items:
		total += cart_item.product.price * cart_item.quality
		quantity = cart_item.quality

	tax = (total / 100) * 2  	# 2% Tax
	grand_total = total + tax

	if request.method == 'POST':
		form = OrderForm(request.POST)
		# print(form.cleaned_data['first_name'])
		if form.is_valid():
			# Store all the billing information inside Order Model
			data = Order()
			data.user = current_user
			data.first_name = form.cleaned_data['first_name']
			data.last_name = form.cleaned_data['last_name']
			data.phone = form.cleaned_data['phone']
			data.email = form.cleaned_data['email']
			data.address_line_1 = form.cleaned_data['address_line_1']
			data.address_line_2 = form.cleaned_data['address_line_2']
			data.country = form.cleaned_data['country']
			data.state = form.cleaned_data['state']
			data.city = form.cleaned_data['city']
			data.order_note = form.cleaned_data['order_note']
			data.order_total = grand_total
			data.tax = tax
			data.ip = request.META.get('REMOTE_ADDR')
			data.save()

			yr = int(datetime.date.today().strftime('%Y'))
			mt = int(datetime.date.today().strftime('%m'))
			dt = int(datetime.date.today().strftime('%d'))

			dat = datetime.date(yr,mt,dt)
			current_date = dat.strftime('%Y%m%d')
			order_number = current_date + str(data.id)

			data.order_number = order_number
			data.save()

			order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

			context = {
				'total':total,
				'tax':tax,
				'grand_total': grand_total,
				'order':order,
				'cart_items':cart_items,
			}

			return render(request, 'orders/payment.html', context)

		else:
			return redirect('cart:cart')



def payment(request):

	body = json.loads(request.body)
	order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
	payment = Payment.objects.create(
		user=request.user, 
		payment_id=body['transID'], 
		payment_method=body['payment_method'],
		amount_paid= order.order_total,
		status=body['status'],
		)

	payment.save()
	order.payment = payment
	order.is_ordered = True
	order.save()

	# Transfering cart item to Orderproduct

	cart_items = CartItem.objects.filter(user=request.user, is_active=True)
	for item in cart_items:
		orderproduct = OrderProduct()
		orderproduct.order = order
		orderproduct.payment = payment
		orderproduct.user = request.user
		orderproduct.product = item.product
		orderproduct.quantity = item.quality
		orderproduct.product_price = item.product.price
		orderproduct.is_ordered = True
		orderproduct.save()

		# Transfering Product Variation to OrderProduct Model

		cart_items = CartItem.objects.get(id=item.id)
		product_variation = cart_items.product_variation.all()
		orderproduct = OrderProduct.objects.get(id=orderproduct.id)
		orderproduct.variation.set(product_variation)
		orderproduct.save()

		# Reducing product quantity
		product = Product.objects.get(id=item.product.id)
		product.stock -= item.quality
		product.save()

	CartItem.objects.filter(user=request.user).delete()

	# Sending order received mail
	to_mail = order.email
	mail_subject = 'Thanks for your order.'
	mail_messages = render_to_string('orders/order_received_mail.html', {
	'order':order,
	})
	
	email_send = EmailMessage(mail_subject, mail_messages, settings.EMAIL_HOST_USER, to=[to_mail])
	email_send.fail_silently = False
	email_send.send()

	# Send Order number and transaction id to sendData via Json response
	data = {
		'order_number': order.order_number,
		'transID': payment.payment_id,
	}

	return JsonResponse(data)


def order_completed(request):
	order_number = request.GET.get('order_number')
	transID = request.GET.get('payment_id')
	payment = Payment.objects.get(payment_id=transID)
	subtotal = 0
	try:
		order = Order.objects.get(order_number=order_number, is_ordered=True)
		orderproduct = OrderProduct.objects.filter(order__id=order.id)
		for i in orderproduct:
			subtotal = i.product_price * i.quantity
		context = {
			'order':order,
			'transID':transID,
			'orderproduct':orderproduct,
			'subtotal':subtotal,
			'payment':payment,
		}

		return render(request, 'orders/order_complete.html', context)

	except:
		return redirect('home')