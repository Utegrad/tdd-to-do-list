from django.test import TestCase

from lists.models import Item


class ListViewTest(TestCase):

    def test_view_list_uses_list_template(self):
        response = self.client.get('/lists/the-only-list/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')

        response = self.client.get('/lists/the-only-list/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
