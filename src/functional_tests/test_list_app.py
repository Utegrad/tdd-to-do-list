import os
import re

import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from functional_tests.helpers import wait_for_page_load

IMPLICIT_WAIT = 5
MAX_WAIT = 8
HOME_PAGE_TITLE = 'To-Do - Home'


@pytest.fixture()
def url_to_test():
    test_url = os.environ.get('TEST_URL')
    return test_url if test_url else 'http://tdd.utegrads.com'


@pytest.fixture()
def browser() -> webdriver:
    ops = Options()
    ops.headless = True
    browser = webdriver.Firefox(options=ops)
    yield browser
    browser.quit()


def almost_equal(value, reference, delta):
    result = False
    upper_limit = reference + delta
    lower_limit = reference - delta
    if lower_limit <= value <= upper_limit:
        result = True
    return result


def test_home_page(browser, url_to_test):
    browser.get(url_to_test)
    assert HOME_PAGE_TITLE in browser.title
    current_url = browser.current_url

    header_text = browser.find_element_by_tag_name('h3').text
    assert 'To-Do' in header_text

    input_box = browser.find_element_by_id('id_new_item')
    assert input_box.get_attribute('placeholder') == 'Enter a to-do item'

    input_string = 'Buy a peacock feather'
    display_string = f'1: {input_string}'
    input_box.send_keys(input_string)
    with wait_for_page_load(browser):
        input_box.send_keys(Keys.ENTER)
    # should have a row with '1: Buy a peacock feather'
    current_url = browser.current_url
    try:
        row_elements = WebDriverWait(browser, MAX_WAIT)\
            .until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'row')))
        assert display_string in [r.text for r in row_elements]
    except TimeoutException:
        pytest.fail(f'Time out when waiting for row with "{display_string}"')

    input_box = browser.find_element_by_id('id_new_item')
    input_string = 'Use a peacock feather to make a fly'
    display_strings = [display_string, f'2: {input_string}']
    input_box.send_keys(input_string)
    with wait_for_page_load(browser):
        input_box.send_keys(Keys.ENTER)

    # should now have two entries with '1: Buy a peacock feather' and 2: Use a peacock feather to make a fly')
    current_url = browser.current_url
    try:
        div_elements = WebDriverWait(browser, MAX_WAIT)\
            .until((ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, id_item_row_)]'))))
        for d in display_strings:
            assert d in [e.text for e in div_elements]
    except TimeoutException:
        pytest.fail(f'Timeout waiting for rows with {display_strings}')


def test_multiple_users_can_start_lists_at_different_urls(browser, url_to_test):
    # first user starts a list
    browser.get(url_to_test)
    # enter first item for list
    input_box = browser.find_element_by_id('id_new_item')
    input_box.send_keys('Buy a peacock feather')
    with wait_for_page_load(browser):
        input_box.send_keys(Keys.ENTER)

    # first user list has unique URL
    first_user_list_url = browser.current_url
    assert re.search(r'/lists/.+', first_user_list_url)

    ## Second user - new browser session
    browser.delete_all_cookies()

    # second user does see first user's list items
    browser.get(url_to_test)
    page_text = browser.find_element_by_tag_name('body').text
    assert 'Buy a peacock feather' not in page_text
    assert 'Use a peacock feather to make a fly' not in page_text

    # second user starts a list
    input_box = browser.find_element_by_id('id_new_item')
    input_box.send_keys('buy milk')
    with wait_for_page_load(browser):
        input_box.send_keys(Keys.ENTER)

    # second user list gets own URL
    second_user_list_url = browser.current_url
    assert re.search(r'/lists/.+', second_user_list_url)
    assert second_user_list_url != first_user_list_url

    # first user list not shown to second user
    page_text = browser.find_element_by_tag_name('body').text
    assert 'Buy a peacock feather' not in page_text
    assert 'buy milk' in page_text

    browser.quit()


def test_layout_and_styling(browser, url_to_test):
    # smoke test to check style sheets load
    browser.get(url_to_test)
    browser.set_window_size(1024, 768)

    input_box = browser.find_element_by_id('id_new_item')
    assert almost_equal(input_box.location['x'] + input_box.size['width'] / 2,
                        512, 10)

    input_box.send_keys('testing')
    with wait_for_page_load(browser):
        input_box.send_keys(Keys.ENTER)
    row_1 = browser.find_element_by_id('id_item_row_1')
    input_box = browser.find_element_by_id('id_new_item')
    assert almost_equal(input_box.location['x'] + input_box.size['width'] / 2,
                        512, 10)
    browser.quit()
