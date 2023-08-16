from django.db import models
from django.core.files import File
from django.contrib.auth.models import User
from itertools import product

from io import BytesIO
from PIL import Image
class category(models.Model):
    name=models.CharField(max_length=279)
    slug=models.SlugField()
    class Meta:
        verbose_name_plural='Categoryies'
        ordering = ('-name',)

    

    def __str__(self):
        return  self.name
class Products(models.Model):
    category=models.ForeignKey(category,related_name='products',on_delete=models.CASCADE)
    name=models.CharField(max_length=279)
    slug=models.SlugField()
    description=models.TextField(blank=True,null=True)
    price=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        verbose_name_plural='Products'
        ordering = ('-created_at',)
   
    
    def __str__(self):
        return self.name
    def get_display_price(self):
        return self.price 
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240x.jpg'
    
    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
    def get_rating(self):
        reviews_total = 0

        for review in self.reviews.all():
            reviews_total += review.rating
        
        if reviews_total > 0:
            return reviews_total / self.reviews.count()
        
        return 0
class Review(models.Model):
    product_name=models.TextField(blank=True,null=True)
    name=models.TextField(blank=True,null=True)
    rating = models.IntegerField(default=3)
    content = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural='Reviews'
        ordering = ('-created_at',)




class Order(models.Model):
    ORDERED = 'ordered'
    SHIPPED = 'shipped'

    STATUS_CHOICES = (
        (ORDERED, 'Ordered'),
        (SHIPPED, 'Shipped')
    )

    user = models.ForeignKey(User, related_name='orders', blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)
    paid_amount = models.IntegerField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)
    class Meta:
        verbose_name_plural='Orders'
        ordering = ('-created_at',)
    def get_total_price(self):
        if self.paid_amount:
            return self.paid_amount / 100
        
        return 0

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)


class Contact(models.Model):

    name=models.CharField(max_length=50,null=True)
    email=models.EmailField()
    message=models.TextField(max_length=500,null=True)
    phone=models.IntegerField()

    def __int__(self):
        return self.name
class visitor(models.Model):
    visit=models.CharField(max_length=19)
    
    class Meta:
        verbose_name_plural='visitors'
        ordering = ('-visit',)
        
    def __str__(self):
        return  self.visit

    





        
