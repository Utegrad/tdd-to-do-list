import sys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from selenium import webdriver

IMPLICIT_WAIT = 5
HOME_PAGE_TITLE = 'Title'


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