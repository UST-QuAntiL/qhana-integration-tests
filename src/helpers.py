from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from src.wrapper import WebElementWrapper


def create_new_experiment(driver: WebDriver, name: str) -> None:
	new_experiment_button = WebElementWrapper.find_with_xpath(
		driver, "//button[span[text()='New Experiment']]")
	new_experiment_button.click()

	WebElementWrapper.find_active_element(driver).set_text(name)

	create_experiment_button = WebElementWrapper.find_with_xpath(
		driver, "//button[span[normalize-space(text())='Create Experiment']]")
	create_experiment_button.click()

	WebElementWrapper.find_with_xpath(driver, "//qhana-experiment").check_existence()


def switch_to_workspace_tab(driver: WebDriver) -> None:
	workspace_tab = WebElementWrapper.find_with_xpath(driver, "//a[span[normalize-space(text())='Workspace']]")
	workspace_tab.click()


def open_plugin(driver: WebDriver, plugin_name: str) -> None:
	plugin_list_item = WebElementWrapper.find_with_xpath(
		driver, f"//span[starts-with(text(), '{plugin_name}')]")
	plugin_list_item.click()


def get_micro_frontend_iframe(driver: WebDriver) -> WebElementWrapper:
	return WebElementWrapper.find_with_xpath(driver, "//iframe[@class='frontend-frame']")


def get_micro_frontend_input_field(driver: WebDriver, field_name: str) -> WebElementWrapper:
	return WebElementWrapper.find_with_xpath(driver, f"//textarea[@name='{field_name}']")


def submit_micro_frontend(driver: WebDriver) -> None:
	submit_button = WebElementWrapper.find_with_xpath(
		driver, "//button[@class='qhana-form-submit'][text()='submit']")
	submit_button.click()


def switch_to_outputs_tab(driver: WebDriver) -> None:
	output_tab = WebElementWrapper.find_with_xpath(driver, "//a[normalize-space(text())='Outputs']")
	output_tab.click()


def get_visualization_iframe(driver: WebDriver, file_name: str) -> WebElementWrapper:
	return WebElementWrapper.find_with_xpath(driver, f"//iframe[contains(@src, '{file_name}')]")


def get_output_file_text(driver: WebDriver, file_name: str) -> str:
	iframe = get_visualization_iframe(driver, file_name)
	iframe.switch_to_frame()
	text = WebElementWrapper.find_with_xpath(driver, "//pre").get_text()
	driver.switch_to.default_content()

	return text


def wait_for_plugin_to_finish_executing(driver: WebDriver, timeout: int) -> None:
	def _check_if_finished(_driver: WebDriver):
		status = _driver.find_element(By.XPATH, "//div[@class='step-status']/span").text

		if status == "PENDING":
			return False

		if status == "SUCCESS":
			return True

		raise RuntimeError(f"status is {status}")

	WebDriverWait(driver, timeout=timeout).until(_check_if_finished)
