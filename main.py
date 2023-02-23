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


class TestPluginExecution(unittest.TestCase):
	def setUp(self) -> None:
		self.driver = webdriver.Firefox()
		self.driver.get("http://localhost:8080")
		self.driver.implicitly_wait(10)

	def tearDown(self) -> None:
		self.driver.close()

	def test_create_new_experiment(self):
		self._create_new_experiment(self.driver, "test")

	def test_hello_world_multi_step(self):
		self._create_new_experiment(self.driver, "test")
		self._switch_to_workspace_tab(self.driver)
		self._open_plugin(self.driver, "hello-world-multi-step")

		self._get_micro_frontend_iframe(self.driver).switch_to_frame()
		self._get_micro_frontend_input_field(self.driver, "inputStr").set_text("input text")
		self._submit_micro_frontend(self.driver)

		self.driver.switch_to.default_content()

		self._get_micro_frontend_iframe(self.driver).switch_to_frame()
		self._submit_micro_frontend(self.driver)

		self.driver.switch_to.default_content()
		self._wait_for_plugin_to_finish_executing(self.driver, 10)
		self._switch_to_outputs_tab(self.driver)

		assert self._get_output_file_text(self.driver, "output1.txt") == "Processed in the preprocessing step: input text"
		assert self._get_output_file_text(self.driver, "output2.txt") == "Processed in the processing step: input text Input from preprocessing: input text"

	@staticmethod
	def _create_new_experiment(driver: WebDriver, name: str) -> None:
		new_experiment_button = WebElementWrapper.find_with_xpath(
			driver, "//button[span[text()='New Experiment']]")
		new_experiment_button.click()

		WebElementWrapper.find_active_element(driver).set_text(name)

		create_experiment_button = WebElementWrapper.find_with_xpath(
			driver, "//button[span[normalize-space(text())='Create Experiment']]")
		create_experiment_button.click()

	@staticmethod
	def _switch_to_workspace_tab(driver: WebDriver) -> None:
		workspace_tab = WebElementWrapper.find_with_xpath(driver, "//a[span[normalize-space(text())='Workspace']]")
		workspace_tab.click()

	@staticmethod
	def _open_plugin(driver: WebDriver, plugin_name: str) -> None:
		plugin_list_item = WebElementWrapper.find_with_xpath(
			driver, f"//span[starts-with(text(), '{plugin_name}')]")
		plugin_list_item.click()

	@staticmethod
	def _get_micro_frontend_iframe(driver: WebDriver) -> WebElementWrapper:
		return WebElementWrapper.find_with_xpath(driver, "//iframe[@class='frontend-frame']")

	@staticmethod
	def _get_micro_frontend_input_field(driver: WebDriver, field_name: str) -> WebElementWrapper:
		return WebElementWrapper.find_with_xpath(driver, f"//textarea[@name='{field_name}']")

	@staticmethod
	def _submit_micro_frontend(driver: WebDriver) -> None:
		submit_button = WebElementWrapper.find_with_xpath(
			driver, "//button[@class='qhana-form-submit'][text()='submit']")
		submit_button.click()

	@staticmethod
	def _switch_to_outputs_tab(driver: WebDriver) -> None:
		output_tab = WebElementWrapper.find_with_xpath(driver, "//a[normalize-space(text())='Outputs']")
		output_tab.click()

	@staticmethod
	def _get_visualization_iframe(driver: WebDriver, file_name: str) -> WebElementWrapper:
		return WebElementWrapper.find_with_xpath(driver, f"//iframe[contains(@src, '{file_name}')]")

	@staticmethod
	def _get_output_file_text(driver: WebDriver, file_name: str) -> str:
		iframe = TestPluginExecution._get_visualization_iframe(driver, file_name)
		iframe.switch_to_frame()
		text = WebElementWrapper.find_with_xpath(driver, "//pre").get_text()
		driver.switch_to.default_content()

		return text

	@staticmethod
	def _wait_for_plugin_to_finish_executing(driver: WebDriver, timeout: int) -> None:
		def _check_if_finished(_driver: WebDriver):
			status = _driver.find_element(By.XPATH, "//div[@class='step-status']/span").text

			if status == "PENDING":
				return False

			if status == "SUCCESS":
				return True

			raise RuntimeError(f"status is {status}")

		WebDriverWait(driver, timeout=timeout).until(_check_if_finished)
