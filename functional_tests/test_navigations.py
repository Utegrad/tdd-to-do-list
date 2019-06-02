import sys
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

IMPLICIT_WAIT = 5
HOME_PAGE_TITLE = 'To-Do'


class NavigationTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver ' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(IMPLICIT_WAIT)

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    # browse the home page
    # home page title is correct
    def test_home_page(self):
        self.browser.get(self.live_server_url)
        self.assertIn(HOME_PAGE_TITLE, self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        input_box.send_keys('Buy a peacock feather')
        input_box.send_keys(Keys.ENTER)
        time.sleep(3)
        self.check_for_row_in_list_table('1: Buy a peacock feather')

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feather to make a fly')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table('1: Buy a peacock feather')
        self.check_for_row_in_list_table('2: Use peacock feather to make a fly')

        self.fail('finish the test')
