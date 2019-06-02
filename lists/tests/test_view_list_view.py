from django.test import TestCase

from lists.models import Item, List


class ListViewTest(TestCase):

    def test_view_list_uses_list_template(self):
        response = self.client.get('/lists/the-only-list/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_all_items(self):
        _list = List.objects.create()
        Item.objects.create(text='item 1', list=_list)
        Item.objects.create(text='item 2', list=_list)

        response = self.client.get('/lists/the-only-list/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
