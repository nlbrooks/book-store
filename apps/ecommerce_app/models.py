from __future__ import unicode_literals
from django.db import models
import bcrypt, re
# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager): 
    def create_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email is not valid"
        db_list = User.objects.filter(email=postData['email'])
        if len(db_list) > 0:
            errors['is_user'] = "Email is already taken"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        if len(postData['confirm_password']) < 8:
            errors['confirm_password'] = (
                "Confirm password should be at least 8 characters")
        if postData['password'] != postData['confirm_password']:
            errors['pw_match'] = "Passwords should match"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email is not valid"
        else:
            db_list = User.objects.filter(email=postData['email'])
            if len(db_list) == 0:
                errors['not_user'] = "Email is not registered to an account"
            else:
                if not bcrypt.checkpw(postData['password'].encode(), 
                db_list[0].password.encode()):
                    errors['pw'] = "Password is incorrect"
        return errors


class Common(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    class Meta:
        abstract = True

class UserCommon(models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    class Meta:
        abstract = True

class Admin(UserCommon, Common):
    pass

class User(UserCommon, Common):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

class Product(Common):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()
    product_image = models.ImageField(upload_to="ecommerce_app/images")

class Author(Common):
    name = models.CharField(max_length=255)

class Book(Product):
    author = models.ForeignKey(Author, related_name="books")

class Order(Common):
    user = models.ForeignKey(User, related_name="orders")
    product = models.ForeignKey(Product, related_name="orders")
    total = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=255)
