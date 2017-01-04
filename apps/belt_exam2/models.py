from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from datetime import datetime, date
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def login(self,post):
        user_list= User.objects.filter(email=post['email'])
        if user_list:
            user=user_list[0]
            #then check for credentials
            if bcrypt.hashpw(post['password'].encode(), user.password.encode()) == user.password:
                return user
        return None

    def register(self, post):
        encrypted_password=bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt())
        User.objects.create(name=post['name'], alias=post['alias'], email=post['email'], password=encrypted_password, date_of_birth=post['date_of_birth'])

    def validate_user_info(self, post):
        today = date.today()
        errors = []

        if len(post['name']) == 0:
            errors.append("Name is required")
        elif len(post['name']) < 3:
            errors.append("Name must be at least 3 characters")
        elif not post['name'].isalpha():
            errors.append("Name must consist of only letters")

        if len(post['alias']) == 0:
            errors.append("Alias is required")
        elif len(post['alias']) < 3:
            errors.append("Alias must be at least 3 characters")
        if len(User.objects.filter(alias=post['alias'])) > 0:
            errors.append("Alias is already taken")

        if len(post['email']) == 0:
            errors.append("Email is required")
        if len(User.objects.filter(email=post['email'])) > 0:
            errors.append("Email is already taken")

        if len(post['password']) == 0:
            errors.append("Password is required")
        elif len(post['password']) < 8:
            errors.append("Password must be at least 8 characters")
        elif post['password'] != post['passconf']:
            errors.append("Password fields must match")

        if not post['date_of_birth']:
            errors.append("Date of Birth is required")
            print "******"
        else:
            try:
                date_of_birth = datetime.strptime(post['date_of_birth'], '%Y-%m-%d')
                print "****** ******"
                if date_of_birth.date() >= today:
                    errors.append("Are you from the future?")
                    print "****** ****** ******"
            except:
                errors.append("Please enter a valid date for the From Date field")
                print "****** ****** ****** ******"
        return errors

class QuoteManager(models.Manager):
    def validate_quote_info(self, post):
        errors = []

        if len(post['author']) == 0:
            errors.append("Author is required")
        elif len(post['author']) < 3:
            errors.append("Author name must be at least 3 characters")

        if len(post['quote']) == 0:
            errors.append("Quote is required")
        elif len(post['quote']) < 10:
            errors.append("Quote must be at least 10 characters")
        return errors


class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    author = models.CharField(max_length=255)
    quote = models.TextField()
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

class Favorited(models.Model):
    favoritor = models.ForeignKey(User)
    quote = models.ForeignKey(Quote, related_name='favorite_quote')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
