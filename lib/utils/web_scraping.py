import time
import random

from datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sys import platform
from . import constants
from .datatype import is_empty_string


class html_input_has_value:
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if element and not is_empty_string(element.get_attribute("value")):
            return element
        else:
            return False


class html_text_has_been_added:
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if element and not is_empty_string(element.text):
            return element
        else:
            return False


def with_random_delay(func, min_delay=0, max_delay=5):
    def new_func(*args):
        result = func(*args)
        random_delay = random.randint(min_delay, max_delay)
        time.sleep(random_delay)
        return result

    return new_func


def is_mac_os():
    return platform == "darwin"


def open_link_in_new_tab(html_link):
    modifier_key = Keys.COMMAND if is_mac_os() else Keys.CONTROL
    html_link.send_keys(modifier_key, Keys.RETURN)


def wait_element_until_visible_by_css_selector(driver, timeout, css_selector):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
        )
    except TimeoutException:
        raise RuntimeError("Cannot find the element[" + css_selector + "] on the page.")
    else:
        return element

def wait_element_until_visible_by_id (driver, timeout, id):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.ID, id))
        )
    except TimeoutException:
        raise RuntimeError("Cannot find the element[" + id + "] on the page.")
    else:
        return element

def wait_elements_until_visible_by_css_selector(driver, timeout, css_selector):
    try:
        elements = WebDriverWait(driver, timeout).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, css_selector))
        )
    except TimeoutException:
        raise RuntimeError(
            "Cannot find the elements[" + css_selector + "] on the page."
        )
    else:
        return elements


def wait_element_until_visible_by_xpath(driver, timeout, xpath):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
    except TimeoutException:
        raise RuntimeError("Cannot find the element[" + xpath + "] on the page.")
    else:
        return element


def wait_elements_until_visible_by_xpath(driver, timeout, xpath):
    try:
        elements = WebDriverWait(driver, timeout).until(
            EC.visibility_of_all_elements_located((By.XPATH, xpath))
        )
    except TimeoutException:
        raise RuntimeError("Cannot find the elements[" + xpath + "] on the page.")
    else:
        return elements


def focus_element(driver, element):
    if element.tag_name == "input":
        element.send_keys("")
    else:
        ActionChains(driver).moveToElement(element).perform()


def parse_date_text(date_text):
    """Parse a date string with format %d/%m/%Y to a dictionary of day, month and year,
    e.g., parse '04/11/2020' to {"day": 4, "month": 11, "year": 2020}
    """
    dmy = date_text.split("/")
    return {"day": int(dmy[0]), "month": int(dmy[1]), "year": int(dmy[2])}


def time_until_end_of_day(dt=None):
    """Get timedelta in seconds until end of day on the datetime passed, or current time."""
    if dt is None:
        dt = datetime.now()
    return (
        ((24 - dt.hour - 1) * 60 * 60) + ((60 - dt.minute - 1) * 60) + (60 - dt.second)
    )