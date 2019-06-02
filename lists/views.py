from django.shortcuts import render, redirect
from lists.models import Item, List


def home_page(request):
    return render(request, 'lists/home.html', )


def view_list(request, list_id):
    _list = List.objects.get(id=list_id)
    items = Item.objects.filter(list=_list)
    return render(request, 'lists/list.html', {'items': items})


def new_list(request):
    _list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=_list)
    return redirect(f'/lists/{_list.id}/')
