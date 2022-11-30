from django import forms
from .models import Order

class OrderForm(forms.ModelForm):

	class Meta:

		model = Order
		fields = ['first_name', 'last_name', 'email', 'phone', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note']
		


	# def __init__(self, *args, **kwargs):

	# 	super(OrderForm, self).__init__(*args, **kwargs)

	# 	self.fields['first_name'].widget.attrs['placeholder']='First Name'
	# 	self.fields['last_name'].widget.attrs['placeholder']='Last Name'
	# 	self.fields['phone'].widget.attrs['placeholder']='Phone'
	# 	self.fields['email'].widget.attrs['placeholder']='example@domain.com'
	# 	self.fields['address_line_1'].widget.attrs['placeholder']='Address 1'
	# 	self.fields['address_line_2'].widget.attrs['placeholder']='Address 2'
	# 	self.fields['country'].widget.attrs['placeholder']='Country'
	# 	self.fields['state'].widget.attrs['placeholder']='State'
	# 	self.fields['city'].widget.attrs['placeholder']='City'

	# 	for field in self.fields:
	# 		self.fields[field].widget.attrs['class'] = 'form-control'

