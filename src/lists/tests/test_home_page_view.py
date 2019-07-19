from django.test import TestCase
from django.urls import resolve, reverse
from django.utils.html import escape

from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from lists.models import Item, List
from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_uses_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get(reverse('home'))
        self.assertIsInstance(response.context['form'], ItemForm)


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post(reverse('lists:new_list'), data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post(reverse('lists:new_list'), data={'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, reverse('lists:view_list', args=[new_list.id]))

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post(reverse('lists:new_list'), data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post(reverse('lists:new_list'), data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post(reverse('lists:new_list'), data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_items_arent_saved(self):
        self.client.post(reverse('lists:new_list'), data={'text ': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
