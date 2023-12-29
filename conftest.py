import os
import json
import time
import pytest
import requests

from helpers.auth_token_helper import get_auth_token
from helpers.runtime_tools import RunTimeTools


# Fixture for the environment configurations
@pytest.fixture(scope="session")
def env_config(pytestconfig):
    return configure_env(pytestconfig)


# Fixture for auth token
@pytest.fixture(scope="session")
def auth_token(env_config):
    return get_auth_token(env_config['client_id'], env_config['client_secret'], env_config['base_url'])


# Fixture for runtime tools
@pytest.fixture(scope="session")
def runtime_tools():
    return RunTimeTools()


def pytest_configure(config):
    requests.urllib3.disable_warnings()

    env_config = configure_env(config)

    try:
        os.makedirs(os.getcwd() + os.sep + "Reports")
    except:
        pass

    current_time = time.strftime("%Y%m%d-%H%M%S")

    config.option.htmlpath = os.getcwd() + os.sep + "Reports" + \
        os.sep + "Report-" + \
        str(env_config['env']).upper() + '-' + current_time + '.html'


def configure_env(config):
    env = None
    with open(os.getcwd() + os.sep + 'environment.json', 'r') as json_file:
        env = json.load(json_file)
        json_file.close()

    return env
