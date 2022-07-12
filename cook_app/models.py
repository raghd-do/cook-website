from django.db import models
import re
from ckeditor.fields import RichTextField


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PW_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')

        if len(postData["user_name"]) < 3:
            errors["user_name"] = "user name cannot be less than 3 characters"

        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Please enter a valid email address"
        else:
            try:
                Chef.objects.get(email=postData["email"])
                errors["email"] = "Email is already exists"
            except:
                pass

        if not PW_REGEX.match(postData["password"]):
            errors["password"] = "password should contain at least more than 8 characters, Upper case, Lower case, and Numbers"

        elif postData["password"] != postData["c_password"]:
            errors["c_password"] = "confirm password doesn't match"

        return errors


class Chef(models.Model):
    pic = models.ImageField(null=True, blank=True, upload_to="users_images/")
    user_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Ingredient(models.Model):
    name = models.CharField(max_length=45)


class Recipe(models.Model):
    img = models.ImageField(upload_to="images/")
    title = models.CharField(max_length=225)
    chef = models.ForeignKey(
        Chef, related_name="recipes", on_delete=models.CASCADE)
    ingredient = models.ManyToManyField(Ingredient, blank=True)
    desc = RichTextField(blank=True, null=True)
    # desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
