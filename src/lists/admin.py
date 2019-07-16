from django.contrib import admin
from .models import List, Item

my_models = [Item, List, ]

admin.site.register(my_models)
