from django.db import models
from accounts.models import Account
from store.models import Product, Variation
# Create your models here.


class Payment(models.Model):

	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	payment_id = models.CharField(max_length=200)
	payment_method = models.CharField(max_length=200)
	amount_paid = models.CharField(max_length=100)
	status = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.payment_id



class Order(models.Model):

	STATUS = {
		('New', 'New'),
		('Accepted', 'Accepted'),
		('Completed', 'Completed'),
		('Cancelled', 'Cancelled'),
	}

	user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
	payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
	order_number = models.CharField(max_length=100)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	phone = models.CharField(max_length=15)
	email = models.EmailField(max_length=50)
	address_line_1 = models.CharField(max_length=100)
	address_line_2 = models.CharField(max_length=100, blank=True, null=True)
	country = models.CharField(max_length=50)
	state = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	order_note = models.CharField(max_length=200)
	order_total = models.FloatField()
	tax = models.FloatField()
	status = models.CharField(choices=STATUS, default='New', max_length=50)
	ip = models.CharField(max_length=30, blank=True)
	is_ordered = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.order_number

	def full_name(self):
		return f'{self.first_name} {self.last_name}'


class OrderProduct(models.Model):

	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	variation = models.ManyToManyField(Variation, blank=True)
	quantity = models.IntegerField()
	product_price = models.IntegerField()
	is_ordered = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.product.product_name

