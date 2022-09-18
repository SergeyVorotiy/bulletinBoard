import datetime
import random

from django.contrib.auth.models import User
from django.core.management.utils import get_random_secret_key
from django.db import models


class Declaration(models.Model):
    CATEGORIES = [
        ('tanks', 'Танки'),
        ('hills', 'Хилы'),
        ('DD', 'ДД'),
        ('merchants', 'Торговцы'),
        ('gildmasters', 'Гилдмастеры'),
        ('cvestgivers', 'Квестгиверы'),
        ('blacksmith', 'Кузнецы'),
        ('tenners', 'Кожевники'),
        ('potioncookers', 'Зельевары'),
        ('spellmasters', 'Мастера заклинаний'),
    ]
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    text = models.TextField()
    category = models.CharField(max_length=16, choices=CATEGORIES, default='tanks')
    upload = models.FileField(upload_to='media/', default='', blank=True)


class DeclarationResponse(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    declaration = models.ForeignKey(Declaration, on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    accepted = models.BooleanField(default=False)


class UserActivation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=256, default=get_random_secret_key())
    user_activated = models.BooleanField(default=False)
