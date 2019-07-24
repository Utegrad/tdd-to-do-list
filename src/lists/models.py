from django.db import models
from django.urls import reverse


class List(models.Model):
    name = models.TextField(max_length=128, default='')

    def get_absolute_url(self):
        return reverse('lists:view_list', args=[self.id])


class Item(models.Model):
    text = models.TextField(default='', )
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('text', 'list')
        ordering = ('id', )

    def __str__(self):
        return self.text
