import time
from contextlib import contextmanager

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait

MAX_WAIT = 3


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


@contextmanager
def wait_for_page_load(browser, timeout=3):
    """ Wait for a page load.
        Taken from: http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html
    """
    old_page = browser.find_element_by_tag_name('html')
    yield
    WebDriverWait(browser, timeout).until(
        staleness_of(old_page)
    )
