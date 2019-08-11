from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse

from lists.forms import ItemForm, ExistingListItemForm
from lists.models import Item, List


def home_page(request):
    return render(request, 'lists/home.html', {'form': ItemForm()})


def view_list(request, list_id):
    _list = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=_list)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=_list, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(_list)
    return render(request, 'lists/list.html', {'list': _list, 'form': form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'lists/home.html', {'form': form})
