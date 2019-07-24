from unittest import TestCase
from django.core.exceptions import ValidationError

import pytest
from django.urls import reverse

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

    @pytest.mark.django_db
    def test_get_absolute_url(self):
        _list = List.objects.create()
        self.assertEqual(_list.get_absolute_url(), reverse('lists:view_list', args=[_list.id, ]))


class ItemModelTest(TestCase):

    @pytest.mark.django_db
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    @pytest.mark.django_db
    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    @pytest.mark.django_db
    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.full_clean()
            item.save()

    @pytest.mark.django_db
    def test_duplicate_items_in_same_list_are_invalid(self):
        item_text = 'blah'
        list_ = List.objects.create()
        Item.objects.create(list=list_, text=item_text)
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text=item_text)
            item.full_clean()

    @pytest.mark.django_db
    def test_CAN_save_duplicate_item_to_seperate_list(self):
        item_text = 'blah'
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text=item_text)
        item = Item(list=list2, text=item_text)
        item.full_clean()  # should not raise

    @pytest.mark.django_db
    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='_a')
        item2 = Item.objects.create(list=list1, text='_b')
        item3 = Item.objects.create(list=list1, text='_c')
        self.assertEqual(
            list(Item.objects.filter(list__pk=list1.id)),
            [item1, item2, item3]
        )
        self.assertEqual(
            list(list1.item_set.all()),  # another way to get the queryset based on the ForeignKey relationship
            [item1, item2, item3]
        )

    @pytest.mark.django_db
    def test_string_representation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')
