from django.contrib import admin
from .models import *


class ChefAdmin(admin.ModelAdmin):
    list_display = ['user_name']


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title']


class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Chef, ChefAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
