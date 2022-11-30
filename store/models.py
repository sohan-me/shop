from django.db import models
from core.models import Category
from django.urls import reverse
# Create your models here.


class Product(models.Model):

    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.PositiveIntegerField()
    images = models.ImageField(upload_to='photos/product')
    stock = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('store:product_details', args=[self.category.slug, self.slug])


class VariationsManager(models.Manager):

    def colors(self):
        return super(VariationsManager, self).filter(variation_category='color', is_available=True)

    def sizes(self):
        return super(VariationsManager, self).filter(variation_category='size', is_available=True)



variation_category_choices = (
            ('color','color'),
            ('size','size'),
    ) 


class Variation(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=200, choices=variation_category_choices)
    variation_value = models.CharField(max_length=200, default='Single')
    is_available = models.BooleanField(default=True)

    objects = VariationsManager()

    def __str__(self):
        return f'{self.variation_category} {self.variation_value}'