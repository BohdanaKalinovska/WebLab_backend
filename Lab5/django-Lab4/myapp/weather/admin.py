from django.contrib import admin
#Імпортуємо клас City з models.py
from .models import City
admin.site.register(City)
