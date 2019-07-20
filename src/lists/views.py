from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse

from lists.forms import ItemForm
from lists.models import Item, List


def home_page(request):
    return render(request, 'lists/home.html', {'form': ItemForm()})


def view_list(request, list_id):
    _list = List.objects.get(id=list_id)
    form = ItemForm()
    error = None
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST['text'], list=_list)
            return redirect(_list)
    return render(request, 'lists/list.html', {'list': _list, 'form': form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    else:
        return render(request, 'lists/home.html', {'form': form})
