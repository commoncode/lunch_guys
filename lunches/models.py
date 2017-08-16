from django.db import models
from django.utils import timezone


class Menu(models.Model):
    day = models.DateField(unique=True, default=timezone.now)
    items = models.ManyToManyField('Item')

    def __str__(self):
        return str(self.day)


class Item(models.Model):
    stock = models.IntegerField()
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=255)

    def __str__(self):
        return '{} ({})'.format(self.title, self.stock)


class Order(models.Model):
    name = models.CharField(max_length=20)
    item = models.ForeignKey('Item')

    def __str__(self):
        return '{}: {}'.format(self.pk, self.name)
