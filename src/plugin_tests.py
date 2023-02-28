import os
import unittest

from selenium import webdriver

from src import helpers


class TestPluginExecution(unittest.TestCase):
	options = {
		"firefox": webdriver.FirefoxOptions(),
		"chrome": webdriver.ChromeOptions(),
	}

	def setUp(self) -> None:
		browser = os.environ.get("INTEGRATION_TEST_BROWSER", "firefox")
		remote = os.environ.get("INTEGRATION_TEST_REMOTE", "false").lower() == "true"

		if remote:
			remote_url = os.environ.get("INTEGRATION_TEST_REMOTE_URL", "http://localhost:4444")
			self.driver = webdriver.Remote(command_executor=remote_url, options=self.options[browser])
		else:
			if browser == "firefox":
				self.driver = webdriver.Firefox(options=self.options[browser])
			elif browser == "chrome":
				self.driver = webdriver.Chrome(options=self.options[browser])
			else:
				raise ValueError(f"unsupported browser {browser}")

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
		helpers.get_micro_frontend_text_area(self.driver, "inputStr").set_text("input text")
		helpers.submit_micro_frontend(self.driver)

		self.driver.switch_to.default_content()

		helpers.get_micro_frontend_iframe(self.driver).switch_to_frame()
		helpers.submit_micro_frontend(self.driver)

		self.driver.switch_to.default_content()
		helpers.wait_for_plugin_to_finish_executing(self.driver, 100)
		helpers.switch_to_outputs_tab(self.driver)

		assert helpers.get_output_file_text(self.driver, "output1.txt") == "Processed in the preprocessing step: input text"
		assert helpers.get_output_file_text(self.driver, "output2.txt") == "Processed in the processing step: input text Input from preprocessing: input text"

	def test_muse(self):
		# Costume Loader
		helpers.create_new_experiment(self.driver, "test")
		helpers.switch_to_workspace_tab(self.driver)
		helpers.open_plugin(self.driver, "Costume loader")

		helpers.get_micro_frontend_iframe(self.driver).switch_to_frame()
		helpers.get_micro_frontend_input(self.driver, "dbHost").set_text("muse-db")
		helpers.get_micro_frontend_input(self.driver, "dbUser").set_text("test")
		helpers.get_micro_frontend_input(self.driver, "dbPassword").set_text("test")
		helpers.get_micro_frontend_input(self.driver, "dbDatabase").set_text("KostuemRepo")

		helpers.submit_micro_frontend(self.driver)

		self.driver.switch_to.default_content()
		helpers.wait_for_plugin_to_finish_executing(self.driver, 100)
		helpers.switch_to_outputs_tab(self.driver)

		# Wu Palmer similarities
		helpers.switch_to_workspace_tab(self.driver)
		helpers.open_plugin(self.driver, "Wu Palmer similarities")

		helpers.choose_file(self.driver, "entities_url", "entities.json")
		helpers.choose_file(self.driver, "entities_metadata_url", "attribute_metadata.json")
		helpers.choose_file(self.driver, "taxonomies_zip_url", "taxonomies.zip")

		helpers.get_micro_frontend_iframe(self.driver).switch_to_frame()
		helpers.get_micro_frontend_text_area(self.driver, "attributes").set_text(
			"dominanteFarbe\ndominanterZustand\ndominanteCharaktereigenschaft\ndominanterAlterseindruck\ngenre")
		helpers.submit_micro_frontend(self.driver)
		self.driver.switch_to.default_content()
		helpers.wait_for_plugin_to_finish_executing(self.driver, 100)

		# Sym Max Mean attribute comparer
		helpers.switch_to_workspace_tab(self.driver)
		helpers.open_plugin(self.driver, "Sym Max Mean attribute comparer")

		helpers.choose_file(self.driver, "entities_url", "entities.json")
		helpers.choose_file(self.driver, "element_similarities_url", "wu_palmer.zip")
		helpers.get_micro_frontend_iframe(self.driver).switch_to_frame()
		helpers.get_micro_frontend_text_area(self.driver, "attributes").set_text(
			"dominanteFarbe\ndominanterZustand\ndominanteCharaktereigenschaft\ndominanterAlterseindruck\ngenre")
		helpers.submit_micro_frontend(self.driver)
		self.driver.switch_to.default_content()
		helpers.wait_for_plugin_to_finish_executing(self.driver, 100)

		# Similarities to distances transformers
		helpers.switch_to_workspace_tab(self.driver)
		helpers.open_plugin(self.driver, "Similarities to distances transformers")

		helpers.choose_file(self.driver, "attribute_similarities_url", "sym_max_mean.zip")
		helpers.get_micro_frontend_iframe(self.driver).switch_to_frame()
		helpers.get_micro_frontend_text_area(self.driver, "attributes").set_text(
			"dominanteFarbe\ndominanterZustand\ndominanteCharaktereigenschaft\ndominanterAlterseindruck\ngenre")
		helpers.submit_micro_frontend(self.driver)
		self.driver.switch_to.default_content()
		helpers.wait_for_plugin_to_finish_executing(self.driver, 100)

		# Aggregators
		helpers.switch_to_workspace_tab(self.driver)
		helpers.open_plugin(self.driver, "Aggregators")

		helpers.choose_file(self.driver, "attribute_distances_url", "attr_dist.zip")
		helpers.get_micro_frontend_iframe(self.driver).switch_to_frame()
		helpers.submit_micro_frontend(self.driver)
		self.driver.switch_to.default_content()
		helpers.wait_for_plugin_to_finish_executing(self.driver, 100)

		# Multidimensional Scaling (MDS)
		helpers.switch_to_workspace_tab(self.driver)
		helpers.open_plugin(self.driver, "Multidimensional Scaling (MDS)")

		helpers.choose_file(self.driver, "entity_distances_url", "entity_distances.json")
		helpers.get_micro_frontend_iframe(self.driver).switch_to_frame()
		helpers.submit_micro_frontend(self.driver)
		self.driver.switch_to.default_content()
		helpers.wait_for_plugin_to_finish_executing(self.driver, 100)

		# Quantum k-means
		helpers.switch_to_workspace_tab(self.driver)
		helpers.open_plugin(self.driver, "Quantum k-means")

		helpers.choose_file(self.driver, "entity_points_url", "entity_points.json")
		helpers.get_micro_frontend_iframe(self.driver).switch_to_frame()
		helpers.submit_micro_frontend(self.driver)
		self.driver.switch_to.default_content()
		helpers.wait_for_plugin_to_finish_executing(self.driver, 100)
