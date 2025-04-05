from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator,MaxValueValidator
from  django.contrib.auth.models import User
from rest_framework import serializers


def alphanumberic(value):
    if not str(value).isalnum():
        raise serializers.ValidationError("Only alphanumberic characters are allowed")
    return value

class Showroomlist(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name
  

class Carlist(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)  # Allowing blank descriptions
    active = models.BooleanField(default=False)
    chassisnumber = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    showroom = models.ForeignKey(Showroomlist, on_delete=models.CASCADE, related_name="showrooms", null=True) # Corrected related_name to lowercase for consistency

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"

# Create your models here.
# class Carlist(models.Model):
#     name =  models.CharField(max_length=50)
#     description = models.CharField(max_length=200)
#     active = models.BooleanField(default=False)
#     chassisnumber = models.CharField(max_length=100,blank=True,null=True)
#     price = models.DecimalField(max_digits=9,decimal_places=2,blank=True,null=True)
#     showroom =models.ForeignKey(Showroomlist,on_delete=models.CASCADE,related_name="Showrooms",null=True)
#     def __str__(self):
#         return self.name

# Review -- one to many relationship  or many to one
# class Review(models.Model):
#     apiuser = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
#     rating = models.IntegerField(validators=[MaxValueValidator(5),MinValueValidator(1)])
#     comments = models.CharField(max_length=200,null=True)
#     car = models.ForeignKey(Carlist,on_delete=models.CASCADE,related_name="Reviews",null=True)
#     create = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
   
#     def __str__(self):
#         return "The rating of" + self.car.name +":---"+str(self.rating)~

class Review(models.Model):
    apiuser = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    comments = models.TextField(null=True, blank=True)  # Changed to TextField
    car = models.ForeignKey(Carlist, on_delete=models.CASCADE, related_name="reviews", null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"The rating of {self.car.name if self.car else 'Unknown Car'}: {self.rating}"

        

