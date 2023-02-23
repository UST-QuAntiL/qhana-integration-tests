import unittest

from selenium import webdriver

import helpers


class TestPluginExecution(unittest.TestCase):
	def setUp(self) -> None:
		self.driver = webdriver.Firefox()
		self.driver.get("http://localhost:8080")
		self.driver.implicitly_wait(10)

	def tearDown(self) -> None:
		self.driver.quit()

	def test_create_new_experiment(self):
		helpers.create_new_experiment(self.driver, "test")

	def test_hello_world_multi_step(self):
		helpers.create_new_experiment(self.driver, "test")
		helpers.switch_to_workspace_tab(self.driver)
		helpers.open_plugin(self.driver, "hello-world-multi-step")

		helpers.get_micro_frontend_iframe(self.driver).switch_to_frame()
		helpers.get_micro_frontend_input_field(self.driver, "inputStr").set_text("input text")
		helpers.submit_micro_frontend(self.driver)

		self.driver.switch_to.default_content()

		helpers.get_micro_frontend_iframe(self.driver).switch_to_frame()
		helpers.submit_micro_frontend(self.driver)

		self.driver.switch_to.default_content()
		helpers.wait_for_plugin_to_finish_executing(self.driver, 10)
		helpers.switch_to_outputs_tab(self.driver)

		assert helpers.get_output_file_text(self.driver, "output1.txt") == "Processed in the preprocessing step: input text"
		assert helpers.get_output_file_text(self.driver, "output2.txt") == "Processed in the processing step: input text Input from preprocessing: input text"
