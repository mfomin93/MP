# # #
# Control API Fault Insertion Upgrade Testing
# # #

import pytest
from random import randint
import time
import controlapi
import sys
sys.path.insert(0, '../../utils/ping.py')
from utils.ping import Ping

import threading

MAX_RUNS = 10

def stop_fault_insertion_thread(th):
    th.UPGRADING = False
    th.join()

def fault_insertion_thread(device_info, masterpower_client):
    th = threading.currentThread()

    bank = device_info["power"]
    outlet = str(bank[1])
    print("Test device is using outlet " + str(outlet) + " on Main Outlet Bank")

    api = "!OutletSet=" + outlet + ",RESET"

    # Give some time for first upgrade to begin
    random = randint(30, 60)
    print("Starting fault insertion in " + str(random) + " seconds!")
    time.sleep(random)

    while getattr(th, "UPGRADING", True):

        print("Resetting outlet! WHOOPS!")
        masterpower_client.send(api + "\n")
        time.sleep(1)
        masterpower_client.receive()
        print("Outlet reset! UH OH!")

        random = randint(45, 120)
        print("Fault insertion thread sleeping for " + str(random) + " seconds...")
        time.sleep(random)

    print("Thread done")


def test_upgrade_fault_insertion(device_info, client, masterpower_client):

    # Fetch current model
    model = controlapi.get_model(client)
    assert model != ""

    # Start fault insertion thread
    th = threading.Thread(target=fault_insertion_thread, args=(device_info, masterpower_client,))
    th.start()

    # Set global timeout for client
    client.timeout(30)

    # Start upgrade loop
    for run in range(MAX_RUNS):

        # Fetch current version
        version = controlapi.get_version(client)
        assert version != ""

        print("Model: " + model + "Version: " + version + "Run: " + str(run+1) + "\n")

        url = controlapi.get_upgrade_url_from_model(model)

        if url == "":
            pytest.skip("No firmware url found for model " + model.rstrip())

        api = "!FirmwareUpdate=" + url

        client.send(api + "\n")
        time.sleep(1)
        res = client.receive()

        if res.rstrip() == controlapi.ERROR:
            stop_fault_insertion_thread(th)
            print("CRITICAL!!! Firmware error by model " + model.rstrip() + " version " + version.rstrip() + " api call " + api)

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

        # Fetch current version
        new_version = controlapi.get_version(client)
        if version.rstrip() != new_version.rstrip():
            stop_fault_insertion_thread(th)
            pytest.fail("CRITICAL!!! Current firmware and new firmware version are different!")

    stop_fault_insertion_thread(th)
    client.timeout(None)