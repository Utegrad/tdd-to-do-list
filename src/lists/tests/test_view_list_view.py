from django.test import TestCase
from django.urls import reverse

from lists.models import Item, List


class ListViewTest(TestCase):

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
