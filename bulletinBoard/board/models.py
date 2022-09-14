from django.contrib.auth.models import User
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
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    text = models.TextField()
    category = models.CharField(max_length=16, choices=CATEGORIES, default='tanks')


class DeclarationResponse(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    declaration = models.ForeignKey(Declaration, on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    accepted = models.BooleanField(default=False)
