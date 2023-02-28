import os
import time
from typing import Callable

from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

SLEEP_TIME = float(os.environ.get("INTEGRATION_TEST_SLEEP_TIME", 1))


class WebElementWrapper:
	def __init__(self, driver: WebDriver, find_method: Callable[[], WebElement]):
		self.driver = driver
		self.find_method = find_method

	@staticmethod
	def find_with_xpath(driver: WebDriver, xpath: str) -> "WebElementWrapper":
		def _find_method() -> WebElement:
			return driver.find_element(By.XPATH, xpath)

		return WebElementWrapper(driver, _find_method)

	@staticmethod
	def find_active_element(driver: WebDriver) -> "WebElementWrapper":
		def _find_method() -> WebElement:
			return driver.switch_to.active_element

		return WebElementWrapper(driver, _find_method)

	def click(self) -> None:
		try:
			time.sleep(SLEEP_TIME)
			element = self.find_method()
			element.click()
		except StaleElementReferenceException:
			print("INFO: caught StaleElementReferenceException")
			self.click()

	def switch_to_frame(self) -> None:
		try:
			time.sleep(SLEEP_TIME)
			element = self.find_method()
			self.driver.switch_to.frame(element)
		except StaleElementReferenceException:
			print("INFO: caught StaleElementReferenceException")
			self.switch_to_frame()

	def get_text(self) -> str:
		try:
			time.sleep(SLEEP_TIME)
			element = self.find_method()

			return element.text
		except StaleElementReferenceException:
			print("INFO: caught StaleElementReferenceException")
			return self.get_text()

	def set_text(self, text: str) -> None:
		try:
			time.sleep(SLEEP_TIME)
			element = self.find_method()
			element.send_keys(text)
		except StaleElementReferenceException:
			print("INFO: caught StaleElementReferenceException")
			self.set_text(text)

	def check_existence(self):
		time.sleep(SLEEP_TIME)
		self.find_method()
