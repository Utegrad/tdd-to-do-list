from unittest import skip

from django.test import TestCase
from django.urls import reverse
from django.utils.html import escape

from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from lists.models import Item, List


class ListViewTest(TestCase):

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            reverse('lists:view_list', args=[list_.id, ]),
            data={'text': ''}
        )

    def test_view_list_uses_list_template(self):
        _list = List.objects.create(name='foo')
        response = self.client.get(reverse('lists:view_list', args=[_list.id]))
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_only_items_for_a_list(self):
        correct_list = List.objects.create(name='a list')
        Item.objects.create(text='item 1', list=correct_list)
        Item.objects.create(text='item 2', list=correct_list)
        other_list = List.objects.create(name='other list')
        Item.objects.create(text='item a', list=other_list)
        Item.objects.create(text='item b', list=other_list)

        response = self.client.get(reverse('lists:view_list', args=[correct_list.id]))

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'item a')
        self.assertNotContains(response, 'item b')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create(name='some list')
        correct_list = List.objects.create(name='correct list')
        response = self.client.get(reverse('lists:view_list', args=[correct_list.id]))
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        # create two lists
        correct_list_item_text = 'A new item for an existing list'
        other_list = List.objects.create(name='other list')
        correct_list = List.objects.create(name='correct list')

        # add one item
        self.client.post(
            reverse('lists:view_list', args=[correct_list.id, ]),
            data={'text': correct_list_item_text}
        )

        # check only one item exists, check that item is the only item in the list
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, correct_list_item_text)
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list_name = 'abc123'
        correct_list_name = '123xyz'
        correct_list_item_text = 'new item for correct list'
        other_list = List.objects.create(name=other_list_name)
        correct_list = List.objects.create(name=correct_list_name)

        response = self.client.post(
            reverse('lists:view_list', args=[correct_list.id, ]),
            data={'text': correct_list_item_text}
        )

        self.assertRedirects(response, reverse('lists:view_list', args=[correct_list.id]))

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(reverse('lists:view_list', args=[list_.id, ]))
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    @skip
    def test_duplicate_item_validation_errors_show_on_lists_page(self):
        first_item_text = 'first item'
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text=first_item_text)
        response = self.client.post(
            reverse('lists:view_list', args=[list1.id, ]),
            data={'text': first_item_text}
        )
        expected_error = 'duplicate'
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'lists/list.html')
        self.assertEqual(Item.objects.all().count(), 1)
