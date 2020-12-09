# conftest.py

import pytest
import yaml
import re

def pytest_generate_tests(metafunc):
    if "count" in metafunc.fixturenames:
        with open('config/testrack.yaml') as yaml_file:
            rack_config = yaml.safe_load(yaml_file)
            model = metafunc.config.option.model
            for device in rack_config["devices_under_test"]:
                if device["model"] == model:
                    count = re.findall("[0-9]+", model[::-2])
                    metafunc.parametrize("count", range(1, int(count[0]) + 1))