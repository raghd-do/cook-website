from django import forms
from django.forms import ModelForm
from .models import *


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('img', 'title', 'desc',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'cols': "30", 'rows': "5"}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['img'].widget.attrs.update({'class': 'form-control'})


class create_user(ModelForm):
    class Meta:
        model = Chef
        fields = ('pic', 'user_name', 'email', 'password',)
        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['pic'].widget.attrs.update({'class': 'form-control'})
