import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


class TestPluginExecution(unittest.TestCase):
	def test_hello_world_multi_step(self):
		driver = webdriver.Firefox()
		driver.get("http://localhost:8080")
		driver.implicitly_wait(10)

		try:
			new_experiment_button = driver.find_element(By.XPATH, "//button[span[text()='New Experiment']]")
			new_experiment_button.click()

			driver.switch_to.active_element.send_keys("test")

			create_experiment_button = driver.find_element(By.XPATH, "//button[span[normalize-space(text())='Create Experiment']]")
			create_experiment_button.click()

			workspace_tab = driver.find_element(By.XPATH, "//a[span[normalize-space(text())='Workspace']]")
			workspace_tab.click()

			time.sleep(1)
			hello_world_multi_step_list_item = driver.find_element(By.XPATH, "//span[starts-with(text(), 'hello-world-multi-step')]")

			hello_world_multi_step_list_item.click()

			frontend_iframe = driver.find_element(By.XPATH, "//iframe[@class='frontend-frame']")
			driver.switch_to.frame(frontend_iframe)

			input_field = driver.find_element(By.XPATH, "//textarea[@name='inputStr']")
			input_field.send_keys("input text")

			submit_button = driver.find_element(By.XPATH, "//button[@class='qhana-form-submit'][text()='submit']")
			submit_button.click()

			driver.switch_to.default_content()

			substep1_iframe = WebDriverWait(driver, timeout=10).until(self._get_frontend_iframe)
			driver.switch_to.frame(substep1_iframe)

			time.sleep(1)
			substep1_submit_button = driver.find_element(By.XPATH, "//button[@class='qhana-form-submit'][text()='submit']")
			substep1_submit_button.click()

			driver.switch_to.default_content()

			WebDriverWait(driver, timeout=10).until(self._check_if_finished)

			output_tab = driver.find_element(By.XPATH, "//a[normalize-space(text())='Outputs']")
			output_tab.click()

			preview_iframe1 = driver.find_element(By.XPATH, "//iframe[contains(@src, 'output1.txt')]")
			driver.switch_to.frame(preview_iframe1)

			output_text1 = driver.find_element(By.XPATH, "//pre")
			assert output_text1.text == "Processed in the preprocessing step: input text"
			driver.switch_to.default_content()

			preview_iframe2 = driver.find_element(By.XPATH, "//iframe[contains(@src, 'output2.txt')]")
			driver.switch_to.frame(preview_iframe2)

			output_text2 = driver.find_element(By.XPATH, "//pre")
			assert output_text2.text == "Processed in the processing step: input text Input from preprocessing: input text"
			driver.switch_to.default_content()
		except Exception as e:
			raise e
		finally:
			driver.close()

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
