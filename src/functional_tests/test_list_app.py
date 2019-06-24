import os
import sys

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from functional_tests.helpers import wait_for_page_load

IMPLICIT_WAIT = 5
MAX_WAIT = 8
HOME_PAGE_TITLE = 'To-Do - Home'