import sys
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

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy a peacock feather' for row in rows),
            "New to-do item did not appear in table"
        )

        self.fail('finish the test')