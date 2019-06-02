import sys
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

IMPLICIT_WAIT = 5
MAX_WAIT = 5
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

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

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
        self.wait_for_row_in_list_table('1: Buy a peacock feather')

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feather to make a fly')
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('2: Use peacock feather to make a fly')
        self.wait_for_row_in_list_table('1: Buy a peacock feather')


    def test_multiple_users_can_start_lists_at_different_urls(self):
        # first user starts a list
        self.browser.get(self.live_server_url)
        # enter first item for list
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy a peacock feather')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy a peacock feather')

        # first user list has unique URL
        first_user_list_url = self.browser.current_url
        self.assertRegex(first_user_list_url, '/lists/.+')

        ## Second user - new browser session
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # second user does see first user's list items
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy a peacock feather', page_text)
        self.assertNotIn('Use peacock feather to make a fly', page_text)

        # second user starts a list
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('buy milk')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: buy milk')

        # second user list gets own URL
        second_user_list_url = self.browser.current_url
        self.assertRegex(second_user_list_url, '/lists/.+')
        self.assertNotEqual(second_user_list_url, first_user_list_url)

        # first user list not shown to second user
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy a peacock feather', page_text)
        self.assertIn('buy milk', page_text)

        self.fail('WIP')
