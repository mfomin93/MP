# conftest.py

import pytest
import time
import controlapi
from client import Client

CONTROL_PORT = 23

@pytest.fixture(scope='session')
def device_info(request, rack_config):
    model = request.config.getoption("model")

    if model == "":
        pytest.skip("Model argument required")

    for device in rack_config["devices_under_test"]:
        if device["model"] == model:
            return device

@pytest.fixture(scope='session')
def client(request, rack_config):
    model = request.config.getoption("model")

    if model == "":
        pytest.skip("Model argument required")

    c = Client()

    c.port = controlapi.PORT

    for device in rack_config["devices_under_test"]:
        if device["model"] == model:
            c.ip = device["ip"]
            c.username = device["credentials"]["username"]
            c.password = device["credentials"]["password"]

    if c.ip == "":
        pytest.skip("No IP device found for model " + model)

    c.connect()

    if c.username != "" and c.password != "":
        controlapi.login(c)
    else:
        print("Login Skipped")

    def disconnect():
        c.disconnect()

    request.addfinalizer(disconnect)

    return c

@pytest.fixture(scope='session')
def masterpower_client(request, rack_config):

    name = "Main Outlet Bank"

    c = Client()

    c.port = controlapi.PORT

    for k, v in rack_config["test_equipment"].items():
        if k == "power":
            if v[0]["name"] == name:
                c.ip = v[0]["ip"]
                c.username = v[0]["credentials"]["username"]
                c.password = v[0]["credentials"]["password"]

    if c.ip == "":
        pytest.skip("No IP device found for model " + name)

    c.connect()

    if c.username != "" and c.password != "":
        controlapi.login(c)
    else:
        print("Login Skipped")

    def disconnect():
        c.disconnect()

    request.addfinalizer(disconnect)

    return c