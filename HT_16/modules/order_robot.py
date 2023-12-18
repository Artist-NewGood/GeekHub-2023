import shutil
import os
from typing import Any
from urllib.parse import urljoin

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OrderRobotSpareBinIndustries:
    MAIN_URL = 'https://robotsparebinindustries.com/'
    ROBOT_ORDER_LINK = '#/robot-order'
    SCREENSHOT_DIR_NAME = 'output'
    OUTPUT_PATH = os.path.join(os.getcwd(), SCREENSHOT_DIR_NAME)
    USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
    WAIT_TIME = 5

    def __init__(self):
        self.driver: webdriver.Chrome

    def __enter__(self):
        self.driver = self.__init__driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()

    def __init__driver(self) -> webdriver:

        service = Service(executable_path=ChromeDriverManager().install())

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_argument(f'--user-agent={self.USER_AGENT}')

        driver = webdriver.Chrome(service=service, options=chrome_options)

        return driver

    def wait_and_click_element(self, by: Any, selector: str, timeout=WAIT_TIME) -> WebElement:
        """Expects the element to be clickable."""

        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, selector))
            )
        except TimeoutException as e:
            print(f'Error: The element "{by}: {selector}" did not appear after {timeout} seconds of waiting')
            exit()

    def order_part(self, head: int, body: int, legs: int, address: str) -> None:
        """Fulfilling an order for robot parts."""

        self.driver.fullscreen_window()
        self.close_popup()
        self.choose_head(head_option=head)
        self.choose_body(body_option=body)
        self.input_legs(legs_number=legs)
        self.input_address(shipping_address=address)
        self.click_preview_button()
        self.click_order_button()
        self.make_screenshot()
        self.click_another_order_button()

    def output_folder(self) -> None:
        """Preparing a catalog for saving screenshots."""

        if os.path.exists(self.OUTPUT_PATH):
            shutil.rmtree(self.OUTPUT_PATH)
        os.makedirs(self.OUTPUT_PATH)

    def open_order_page(self) -> None:
        """Opening the robot order page."""

        self.driver.get(urljoin(self.MAIN_URL, self.ROBOT_ORDER_LINK))

    def close_popup(self) -> None:
        """Closing the pop-up window."""

        self.wait_and_click_element(By.CSS_SELECTOR, "div button.btn.btn-dark").click()

    def choose_head(self, head_option: int) -> None:
        """Selection of the robot head."""

        head_selector = (By.XPATH, '//select[@class="custom-select"]')
        Select(self.wait_and_click_element(*head_selector)).select_by_index(head_option)

    def choose_body(self, body_option: int) -> None:
        """Selection of the robot body."""

        self.wait_and_click_element(By.ID, f'id-body-{body_option}').click()

    def input_legs(self, legs_number: int) -> None:
        """Input the number of legs of the robot."""

        css_selector = "div input[placeholder='Enter the part number for the legs']"
        self.wait_and_click_element(By.CSS_SELECTOR, css_selector).send_keys(legs_number)

    def input_address(self, shipping_address: str) -> None:
        """Entering a shipping address."""

        self.wait_and_click_element(By.ID, 'address').send_keys(shipping_address)

    def click_preview_button(self) -> None:
        """Pressing the order preview button."""

        self.wait_and_click_element(By.ID, 'preview').click()

    def click_order_button(self) -> None:
        """Pressing the order confirmation button (until the order is confirmed)."""

        while True:
            try:
                self.wait_and_click_element(By.CSS_SELECTOR, "button[class='btn btn-primary']").click()
                self.driver.find_element(By.ID, 'order-completion')
                break
            except NoSuchElementException:
                continue

    def make_screenshot(self) -> None:
        """Create a screenshot of the order and place it in a folder with the receipt number."""

        number_order = self.take_number_receipt()

        self.wait_and_click_element(By.ID, 'robot-preview-image').screenshot(
            f'{self.OUTPUT_PATH}/{number_order}_robot.png')

    def take_number_receipt(self) -> str:
        """Retrieving the order number from the receipt."""

        number_order = self.wait_and_click_element(By.CSS_SELECTOR, 'p[class="badge badge-success"]').text
        return number_order

    def click_another_order_button(self) -> None:
        """Pressing the button for a new order."""

        self.wait_and_click_element(By.ID, 'order-another').click()
