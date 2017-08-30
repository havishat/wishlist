# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your models here.
from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
import bcrypt
EMAILisnotvalid = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
passd = re.compile(r'^([^0-9]*|[^A-Z]*)$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class LoginManager(models.Manager):

    def validate_login(self, postData):
        errors = []
        # check DB for post_data['email']
        if len(self.filter(email=postData['email'])) > 0:
            # check this user's password
            user = self.filter(email=postData['email'])[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')

        if errors:
            return errors
        return user

    def validate_registration(self, postData):
        errors = []
        # if len(postData['first_name']) == 0 or len(postData['last_name'])== 0 or len(postData['email'])== 0 or len(postData['password'])== 0 or len(postData['confirm_password'])== 0 : 
        #     errors.append("Cannot be blank!")
        if len(postData['first_name']) < 2:
            errors.append("First Name should be more than 5 characters")
        # if not postData['first_name'].isalpha():
        #     errors.append('First name must be all letters')
        # if not postData['last_name'].isalpha():
        #     errors.append('Last name must be all letters')
        if len(postData['last_name'])< 2 :
            errors.append('Last name must be at least two characters')
        # if not EMAILisnotvalid.match(postData['email']):
        #     errors.append("Invalid Email Address!")
        # if not re.match(NAME_REGEX, postData['first_name']) or not re.match(NAME_REGEX, postData['last_name']):
        #     errors.append('name fields must be letter characters only')
        if len(postData['password']) < 8 :
            errors.append("Password should be more than 8 characters")
        if passd.match(postData['password']):
            errors.append("least 1 uppercase letter and 1 numeric value")
        if postData['password'] != postData['password_confirm']:
            errors.append("Password and Password Confirmation are not same")
        if not errors:
        # make our new user
        # hash password
            hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                first_name=postData['first_name'],
                last_name=postData['last_name'],
                email=postData['email'],
                password=hashed
            )
            return new_user
        return errors
# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = LoginManager()
    def __str__(self):
        return self.email

class Item(models.Model):
    item = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    added = models.ForeignKey(User, related_name="added_items")
    wishlist_by = models.ManyToManyField(User, related_name="wishlist_items")