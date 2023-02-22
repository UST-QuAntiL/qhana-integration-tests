import time
import unittest
from typing import Optional, Callable

from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


class WebElementWrapper:
	def __init__(self, driver: WebDriver, find_method: Callable[[], WebElement]):
		self.driver = driver
		self.find_method = find_method

	def click(self) -> None:
		try:
			time.sleep(1)
			element = self.find_method()
			element.click()
		except StaleElementReferenceException:
			print(f"StaleElementReferenceException")
			self.click()

	def switch_to_frame(self) -> None:
		try:
			time.sleep(1)
			element = self.find_method()
			self.driver.switch_to.frame(element)
		except StaleElementReferenceException:
			print(f"StaleElementReferenceException")
			self.switch_to_frame()

	def get_text(self) -> str:
		try:
			time.sleep(1)
			element = self.find_method()

			return element.text
		except StaleElementReferenceException:
			print(f"StaleElementReferenceException")
			return self.get_text()

	def set_text(self, text: str) -> None:
		try:
			time.sleep(1)
			element = self.find_method()
			element.send_keys(text)
		except StaleElementReferenceException:
			print(f"StaleElementReferenceException")
			self.set_text(text)

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


class TestPluginExecution(unittest.TestCase):
	def setUp(self) -> None:
		self.driver = webdriver.Firefox()
		self.driver.get("http://localhost:8080")
		self.driver.implicitly_wait(10)

	def tearDown(self) -> None:
		self.driver.close()

	def test_create_new_experiment(self):
		pass

	def test_hello_world_multi_step(self):
		new_experiment_button = WebElementWrapper.find_with_xpath(self.driver, "//button[span[text()='New Experiment']]")
		new_experiment_button.click()

		WebElementWrapper.find_active_element(self.driver).set_text("test")

		create_experiment_button = WebElementWrapper.find_with_xpath(self.driver, "//button[span[normalize-space(text())='Create Experiment']]")
		create_experiment_button.click()

		workspace_tab = WebElementWrapper.find_with_xpath(self.driver, "//a[span[normalize-space(text())='Workspace']]")
		workspace_tab.click()

		hello_world_multi_step_list_item = WebElementWrapper.find_with_xpath(self.driver, "//span[starts-with(text(), 'hello-world-multi-step')]")
		hello_world_multi_step_list_item.click()

		frontend_iframe = WebElementWrapper.find_with_xpath(self.driver, "//iframe[@class='frontend-frame']")
		frontend_iframe.switch_to_frame()

		input_field = WebElementWrapper.find_with_xpath(self.driver, "//textarea[@name='inputStr']")
		input_field.set_text("input text")

		submit_button = WebElementWrapper.find_with_xpath(self.driver, "//button[@class='qhana-form-submit'][text()='submit']")
		submit_button.click()

		self.driver.switch_to.default_content()

		substep1_iframe = WebElementWrapper.find_with_xpath(self.driver, "//iframe[@class='frontend-frame']")
		substep1_iframe.switch_to_frame()

		substep1_submit_button = WebElementWrapper.find_with_xpath(self.driver, "//button[@class='qhana-form-submit'][text()='submit']")
		substep1_submit_button.click()

		self.driver.switch_to.default_content()

		WebDriverWait(self.driver, timeout=10).until(self._check_if_finished)

		output_tab = WebElementWrapper.find_with_xpath(self.driver, "//a[normalize-space(text())='Outputs']")
		output_tab.click()

		preview_iframe1 = WebElementWrapper.find_with_xpath(self.driver, "//iframe[contains(@src, 'output1.txt')]")
		preview_iframe1.switch_to_frame()

		output_text1 = WebElementWrapper.find_with_xpath(self.driver, "//pre")
		assert output_text1.get_text() == "Processed in the preprocessing step: input text"
		self.driver.switch_to.default_content()

		preview_iframe2 = WebElementWrapper.find_with_xpath(self.driver, "//iframe[contains(@src, 'output2.txt')]")
		preview_iframe2.switch_to_frame()

		output_text2 = WebElementWrapper.find_with_xpath(self.driver, "//pre")
		assert output_text2.get_text() == "Processed in the processing step: input text Input from preprocessing: input text"
		self.driver.switch_to.default_content()

	@staticmethod
	def _get_frontend_iframe(driver: WebDriver) -> WebElement:
		iframe = driver.find_element(By.XPATH, "//iframe[@class='frontend-frame']")

		return iframe

	@staticmethod
	def _check_if_finished(driver: WebDriver):
		status = driver.find_element(By.XPATH, "//div[@class='step-status']/span").text

		if status == "PENDING":
			return False

		if status == "SUCCESS":
			return True

		raise RuntimeError(f"status is {status}")
