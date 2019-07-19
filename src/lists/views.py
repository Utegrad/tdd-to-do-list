from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse

from lists.forms import ItemForm
from lists.models import Item, List


def home_page(request):
    return render(request, 'lists/home.html', {'form': ItemForm()})


def view_list(request, list_id):
    _list = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        try:
            item = Item(text=request.POST['text'], list=_list)
            item.full_clean()
            item.save()
            return redirect(reverse('lists:view_list', args=[_list.id, ]))
        except ValidationError:
            error = "List items can't be blank"
    return render(request, 'lists/list.html', {'list': _list,
                                               'error': error,
                                               'form': ItemForm()})


def new_list(request):
    _list = List.objects.create()
    item = Item.objects.create(text=request.POST['text'], list=_list)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        _list.delete()
        error_msg = "List items can't be blank"
        return render(request, 'lists/home.html', {'error': error_msg,
                                                   'form': ItemForm()})
    return redirect(reverse('lists:view_list', args=[_list.id, ]))
