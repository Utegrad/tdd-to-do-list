from django.db import models


class List(models.Model):
    name = models.TextField(max_length=128, default='')


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
