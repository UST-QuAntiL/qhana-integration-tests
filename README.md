# Integration tests for QHAna

There are two ways to run the integration tests.
In docker containers or on the host machine.

## How to run in docker containers

1. build the required docker images with `docker compose build`
2. have the [QHAna docker compose](https://github.com/UST-QuAntiL/qhana-docker) running
3. start the docker compose of the integration tests with `docker compose up`

To see what is going on inside the Firefox container, open the URL [http://localhost:7900]() in your browser, click on connect and login with the password `secret`.

## How to run on the host machine

1. install [poetry](https://python-poetry.org/)
2. install dependencies with `poetry install`
3. have the [QHAna docker compose](https://github.com/UST-QuAntiL/qhana-docker) running
4. run integration tests on Firefox or Chrome
   1. Firefox: `poetry run python -m unittest plugin_tests`
   2. Chrome: `INTEGRATION_TEST_BROWSER=chrome poetry run python -m unittest plugin_tests`

The first run can take a while to start, because it needs to download the driver for the browser.

## Troubleshooting

If you get timeout errors or errors indicating that an element could not be found, one possible solution could be that you need to increase the sleep time.
To do that change the environment variable `INTEGRATION_TEST_SLEEP_TIME` to a higher value.
For the `integration-tests` container you can do that in the `docker-compose.yml` file and for the command on the host machine you can prepend e.g. `INTEGRATION_TEST_SLEEP_TIME=5`.
