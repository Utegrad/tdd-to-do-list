import sys
from contextlib import contextmanager

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.ui import WebDriverWait

from functional_tests.helpers import wait_for_page_load

IMPLICIT_WAIT = 5
MAX_WAIT = 8
HOME_PAGE_TITLE = 'To-Do - Home'


class NavigationTest(StaticLiveServerTestCase):
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

    @contextmanager
    def wait_for_page_load(self, timeout=IMPLICIT_WAIT):
        """ Wait for a page load.
            Taken from: http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html
        """
        old_page = self.browser.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.browser, timeout).until(
            staleness_of(old_page)
        )

    # browse the home page
    # home page title is correct
    def test_home_page(self):
        self.browser.get(self.live_server_url)
        self.assertIn(HOME_PAGE_TITLE, self.browser.title)
        current_url = self.browser.current_url

        header_text = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('To-Do', header_text)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        input_string = 'Buy a peacock feather'
        display_string = f'1: {input_string}'
        input_box.send_keys(input_string)
        with self.wait_for_page_load():
            input_box.send_keys(Keys.ENTER)
        # should have a row with '1: Buy a peacock feather'
        current_url = self.browser.current_url
        try:
            row_elements = WebDriverWait(self.browser, MAX_WAIT)\
                .until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'row')))
            self.assertIn(display_string, [r.text for r in row_elements])
        except TimeoutException:
            self.fail(f'Time out when waiting for row with "{display_string}"')

        input_box = self.browser.find_element_by_id('id_new_item')
        input_string = 'Use a peacock feather to make a fly'
        display_strings = [display_string, f'2: {input_string}']
        input_box.send_keys(input_string)
        with self.wait_for_page_load():
            input_box.send_keys(Keys.ENTER)

        # should now have two entries with '1: Buy a peacock feather' and 2: Use a peacock feather to make a fly')
        current_url = self.browser.current_url
        try:
            div_elements = WebDriverWait(self.browser, MAX_WAIT)\
                .until((ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, id_item_row_)]'))))
            for d in display_strings:
                self.assertIn(d, [e.text for e in div_elements])
        except TimeoutException:
            self.fail(f'Timeout waiting for rows with {display_strings}')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # first user starts a list
        self.browser.get(self.live_server_url)
        # enter first item for list
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy a peacock feather')
        with self.wait_for_page_load():
            input_box.send_keys(Keys.ENTER)

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
        with self.wait_for_page_load():
            input_box.send_keys(Keys.ENTER)

        # second user list gets own URL
        second_user_list_url = self.browser.current_url
        self.assertRegex(second_user_list_url, '/lists/.+')
        self.assertNotEqual(second_user_list_url, first_user_list_url)

        # first user list not shown to second user
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy a peacock feather', page_text)
        self.assertIn('buy milk', page_text)

        self.fail('WIP')


class NewVisitorTest(StaticLiveServerTestCase):

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

    def test_layout_and_styling(self):
        # smoke test to check style sheets load
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )
        input_box.send_keys('testing')
        with wait_for_page_load(self.browser):
            input_box.send_keys(Keys.ENTER)
        row_1 = self.browser.find_element_by_id('id_item_row_1')
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10,
        )
