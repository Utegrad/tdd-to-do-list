from django.test import TestCase
from django.urls import resolve

from lists.models import Item, List
from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class NewItemTestCase(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        # create two lists
        correct_list_item_text = 'A new item for an existing list'
        other_list = List.objects.create(name='other list')
        correct_list = List.objects.create(name='correct list')

        # add one item
        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': correct_list_item_text}
        )

        # check only one item exists, check that item is the only item in the list
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, correct_list_item_text)
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list_name = 'abc123'
        correct_list_name = '123xyz'
        correct_list_item_text = 'new item for correct list'
        other_list = List.objects.create(name=other_list_name)
        correct_list = List.objects.create(name=correct_list_name)

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': correct_list_item_text}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')