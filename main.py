import time
import unittest

from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


class WebElementWrapper:
	def __init__(self, driver: WebDriver, xpath: str):
		self.element = driver.find_element(By.XPATH, xpath)
		self.driver = driver
		self.xpath = xpath

	def click(self) -> None:
		try:
			time.sleep(1)
			self.element.click()
		except StaleElementReferenceException:
			print(f"StaleElementReferenceException: trying to find {self.xpath}")
			self.element = self.driver.find_element(By.XPATH, self.xpath)
			self.click()

	def switch_to_frame(self) -> None:
		try:
			time.sleep(1)
			self.driver.switch_to.frame(self.element)
		except StaleElementReferenceException:
			print(f"StaleElementReferenceException: trying to find {self.xpath}")
			self.element = self.driver.find_element(By.XPATH, self.xpath)
			self.switch_to_frame()


def _get_active_element(driver: WebDriver) -> WebElement:
	time.sleep(1)
	return driver.switch_to.active_element


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
		new_experiment_button = WebElementWrapper(self.driver, "//button[span[text()='New Experiment']]")
		new_experiment_button.click()

		_get_active_element(self.driver).send_keys("test")

		create_experiment_button = WebElementWrapper(self.driver, "//button[span[normalize-space(text())='Create Experiment']]")
		create_experiment_button.click()

		workspace_tab = WebElementWrapper(self.driver, "//a[span[normalize-space(text())='Workspace']]")
		workspace_tab.click()

		hello_world_multi_step_list_item = WebElementWrapper(self.driver, "//span[starts-with(text(), 'hello-world-multi-step')]")
		hello_world_multi_step_list_item.click()

		frontend_iframe = WebElementWrapper(self.driver, "//iframe[@class='frontend-frame']")
		frontend_iframe.switch_to_frame()

		input_field = self.driver.find_element(By.XPATH, "//textarea[@name='inputStr']")
		input_field.send_keys("input text")

		submit_button = WebElementWrapper(self.driver, "//button[@class='qhana-form-submit'][text()='submit']")
		submit_button.click()

		self.driver.switch_to.default_content()

		substep1_iframe = WebElementWrapper(self.driver, "//iframe[@class='frontend-frame']")
		substep1_iframe.switch_to_frame()

		substep1_submit_button = WebElementWrapper(self.driver, "//button[@class='qhana-form-submit'][text()='submit']")
		substep1_submit_button.click()

		self.driver.switch_to.default_content()

		WebDriverWait(self.driver, timeout=10).until(self._check_if_finished)

		output_tab = WebElementWrapper(self.driver, "//a[normalize-space(text())='Outputs']")
		output_tab.click()

		preview_iframe1 = WebElementWrapper(self.driver, "//iframe[contains(@src, 'output1.txt')]")
		preview_iframe1.switch_to_frame()

		output_text1 = self.driver.find_element(By.XPATH, "//pre")
		assert output_text1.text == "Processed in the preprocessing step: input text"
		self.driver.switch_to.default_content()

		preview_iframe2 = WebElementWrapper(self.driver, "//iframe[contains(@src, 'output2.txt')]")
		preview_iframe2.switch_to_frame()

		output_text2 = self.driver.find_element(By.XPATH, "//pre")
		assert output_text2.text == "Processed in the processing step: input text Input from preprocessing: input text"
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
