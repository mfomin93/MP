# # #
# Control API Firmware Upgrade Test
# # #

import pytest
import time
import controlapi

def test_firmware_upgrade_good_firmware(client):

    # Fetch current model
    model = controlapi.get_model(client)
    assert model != ""

    # Fetch current version
    version = controlapi.get_version(client)
    assert version != ""

    print("Model: " + model + "Version: " + version)

    url = controlapi.get_upgrade_url_from_model(model)
    if url == "":
        pytest.skip("No good firmware url found for model " + model.rstrip())

    api = "!FirmwareUpdate=" + url

    client.send(api + "\n")
    time.sleep(1)
    res = client.receive()

    if res.rstrip() == controlapi.ERROR:
        pytest.fail("CRITICAL!!! Firmware error by model " + model.rstrip() + " version " + version.rstrip() + " api call " + api)

    # Disconnect
    client.disconnect()

    # Wait for device to come back
    print("Waiting " + str(300/60) + " minutes for device to come back online...")
    time.sleep(300)

    # Reconnect on new socket and login
    client.reconnect()

    # Re-login for all models but moip
    if "B-900-MOIP-4K-CTRL" not in model:
        controlapi.login(client)

    # Fetch new version
    new_version = controlapi.get_version(client)
    if version.rstrip() == new_version.rstrip():
        pytest.fail("CRITICAL!!! Current firmware and new firmware version are the same! Upgrade failed!")

def test_firmware_upgrade_empty_url(client):

    # Fetch current model
    model = controlapi.get_model(client)
    assert model != ""

    # Fetch current version
    version = controlapi.get_version(client)
    assert version != ""

    print("Model: " + model + "Version: " + version)

    url = controlapi.EMPTY_URL
    api = "!FirmwareUpdate=" + url

    client.send(api + "\n")
    time.sleep(1)
    res = client.receive()

    if res.rstrip() == controlapi.SUCCESS:
        pytest.fail("CRITICAL!!! Firmware error by model " + model.rstrip() + " version " + version.rstrip() + " api call " + api)

def test_firmware_upgrade_bad_firmware(client):

    # Fetch current model
    model = controlapi.get_model(client)
    assert model != ""

    # Fetch current version
    version = controlapi.get_version(client)
    assert version != ""

    print("Model: " + model + "Version: " + version)

    url = controlapi.BAD_FIRMWARE
    api = "!FirmwareUpdate=" + url

    client.send(api + "\n")
    time.sleep(1)
    res = client.receive()

    if res.rstrip() == controlapi.SUCCESS:
        pytest.fail("CRITICAL!!! Bad Firmware accepted by model " + model.rstrip() + " version " + version.rstrip() + " api call " + api)

def test_firmware_upgrade_bad_url(client):

    # Fetch current model
    model = controlapi.get_model(client)
    assert model != ""

    # Fetch current version
    version = controlapi.get_version(client)
    assert version != ""

    print("Model: " + model + "Version: " + version)

    url = controlapi.NO_FILE
    api = "!FirmwareUpdate=" + url

    client.send(api + "\n")
    time.sleep(1)
    res = client.receive()

    if res.rstrip() == controlapi.SUCCESS:
        pytest.fail("CRITICAL!!! Bad Firmware accepted by model " + model.rstrip() + " version " + version.rstrip() + " api call " + api)