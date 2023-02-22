import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


class TestPluginExecution(unittest.TestCase):
	def setUp(self) -> None:
		self.driver = webdriver.Firefox()

	def tearDown(self) -> None:
		self.driver.close()

	def test_create_new_experiment(self):
		pass

	def test_hello_world_multi_step(self):
		self.driver.get("http://localhost:8080")
		self.driver.implicitly_wait(10)

		new_experiment_button = self.driver.find_element(By.XPATH, "//button[span[text()='New Experiment']]")
		new_experiment_button.click()

		self.driver.switch_to.active_element.send_keys("test")

		create_experiment_button = self.driver.find_element(By.XPATH, "//button[span[normalize-space(text())='Create Experiment']]")
		create_experiment_button.click()

		workspace_tab = self.driver.find_element(By.XPATH, "//a[span[normalize-space(text())='Workspace']]")
		workspace_tab.click()

		time.sleep(1)
		hello_world_multi_step_list_item = self.driver.find_element(By.XPATH, "//span[starts-with(text(), 'hello-world-multi-step')]")

		hello_world_multi_step_list_item.click()

		frontend_iframe = self.driver.find_element(By.XPATH, "//iframe[@class='frontend-frame']")
		self.driver.switch_to.frame(frontend_iframe)

		input_field = self.driver.find_element(By.XPATH, "//textarea[@name='inputStr']")
		input_field.send_keys("input text")

		submit_button = self.driver.find_element(By.XPATH, "//button[@class='qhana-form-submit'][text()='submit']")
		submit_button.click()

		self.driver.switch_to.default_content()

		substep1_iframe = WebDriverWait(self.driver, timeout=10).until(self._get_frontend_iframe)
		self.driver.switch_to.frame(substep1_iframe)

		time.sleep(1)
		substep1_submit_button = self.driver.find_element(By.XPATH, "//button[@class='qhana-form-submit'][text()='submit']")
		substep1_submit_button.click()

		self.driver.switch_to.default_content()

		WebDriverWait(self.driver, timeout=10).until(self._check_if_finished)

		output_tab = self.driver.find_element(By.XPATH, "//a[normalize-space(text())='Outputs']")
		output_tab.click()

		preview_iframe1 = self.driver.find_element(By.XPATH, "//iframe[contains(@src, 'output1.txt')]")
		self.driver.switch_to.frame(preview_iframe1)

		output_text1 = self.driver.find_element(By.XPATH, "//pre")
		assert output_text1.text == "Processed in the preprocessing step: input text"
		self.driver.switch_to.default_content()

		preview_iframe2 = self.driver.find_element(By.XPATH, "//iframe[contains(@src, 'output2.txt')]")
		self.driver.switch_to.frame(preview_iframe2)

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
