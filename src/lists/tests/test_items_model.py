from unittest import TestCase

import pytest

from lists.models import Item, List


class ListModelTest(TestCase):
    @pytest.mark.django_db
    def test_saving_and_retrieving_lists(self):
        first_item_text = 'first item'
        second_item_text = 'second item'
        list_name = 'first list'

        _list = List(name=list_name)
        _list.save()

        first_item = Item(list=_list)
        first_item.text = first_item_text
        first_item.save()

        second_item = Item(list=_list)
        second_item.text = second_item_text
        second_item.save()

        first_list = List.objects.filter(name=list_name).first()
        self.assertEqual(first_list, _list)

        saved_items = Item.objects.filter(list=_list)
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, first_item_text)
        self.assertEqual(first_saved_item.list, _list)
        self.assertEqual(second_saved_item.text, second_item_text)
        self.assertEqual(second_saved_item.list, _list)


class ItemModelTest(TestCase):
    @pytest.mark.django_db
    def test_saving_and_retrieving_items(self):
        first_item_text = 'The first (ever) list item'
        second_item_text = 'Item the second'

        _list = List()
        _list.save()

        first_item = Item(list=_list)
        first_item.text = first_item_text
        first_item.save()

        second_item = Item(list=_list)
        second_item.text = second_item_text
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, first_item_text)
        self.assertEqual(second_saved_item.text, second_item_text)
