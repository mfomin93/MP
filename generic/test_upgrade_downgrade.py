# # #
# Control API Upgrade/Downgrade Testing
# # #

import pytest
import time
import sys

import controlapi

sys.path.insert(0, '../../utils/ping.py')
from utils.ping import Ping

MAX_RUNS = 10

def test_upgrade_downgrade(device_info, client):

    # Fetch current model
    model = controlapi.get_model(client)
    assert model != ""

    # Start upgrade/downgrade loop
    for run in range(MAX_RUNS):

        run_dummy = False

        # Every even run go to dummy, causes
        # test to start out upgrading to dummy
        # and end on the real one
        if run % 2 == 0:
            run_dummy = True

        # Fetch current version
        version = controlapi.get_version(client)
        assert version != ""

        print("Model: " + model + "Version: " + version + "Run: " + str(run+1) + " To Dummy? " + str(run_dummy) + "\n")

        if run_dummy:
            url = controlapi.get_dummy_upgrade_url_from_model(model)
        else:
            url = controlapi.get_upgrade_url_from_model(model)

        if url == "":
            pytest.skip("No firmware url found for model " + model.rstrip())

        api = "!FirmwareUpdate=" + url

        client.send(api + "\n")
        time.sleep(1)
        res = client.receive()

        if res.rstrip() == controlapi.ERROR:
            pytest.fail("CRITICAL!!! Firmware error by model " + model.rstrip() + " version " + version.rstrip() + " api call " + api)

        # Disconnect
        client.disconnect()

        # Wait for device's network to go down
        time.sleep(10)

        # Wait for device to come back
        p = Ping(client.ip)
        while not p.host_up():
            print("Device offline, sleeping 10 seconds...")
            time.sleep(10)
            print("Checking host...")

        print("Device online!")

        # Reconnect on new socket and login
        client.reconnect()

        # Re-login for all models but moip
        if "B-900-MOIP-4K-CTRL" not in model:
            controlapi.login(client)

        # Fetch new version
        new_version = controlapi.get_version(client)
        if version.rstrip() == new_version.rstrip():
            pytest.fail("CRITICAL!!! Current firmware and new firmware version are the same! Upgrade failed!")