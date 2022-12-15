from django.db import models
from core.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg,Count
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

    def avarage(self):
        rating = ReviewRating.objects.filter(product=self, status=True).aggregate(avarage=Avg('rating'))
        avg = 0
        if rating['avarage'] is not None:
            avg = float(rating['avarage'])
        return avg

    def rating_count(self):
        rating = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if rating['count'] is not None:
            count = int(rating['count'])
        return count

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


class ReviewRating(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    review = models.CharField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=100, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review


class ProductImage(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='photos/product', null=True)


    def __str__(self):
        return self.product.product_name


    class Meta:

        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'