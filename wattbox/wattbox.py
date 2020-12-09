# # #
# Control API WattBox Tests
#
# Contains helper functions and constants related to the wattbox control api
#
# # #

import time
import controlapi

APIS = ["?OutletCount", "?OutletStatus", "?OutletName", "?AutoReboot"]

OUTLET_ACTIONS = ["OFF", "ON", "RESET"]

OFF_ON_ACTIONS = ["0", "1"]

# #
# Helpers
# #

def vps_model_check(client):
    # Fetch current model
    model = controlapi.get_model(client)

    for m in controlapi.WATTBOX_VPS_MODELS:
        if model.rstrip() == m:
            return True

    return False

def wifi_model_check(client):
    # Fetch current model
    model = controlapi.get_model(client)

    for m in controlapi.WATTBOX_WIFI_MODELS:
        if model.rstrip() == m:
            return True

    return False

def get_upsconnection(client):
    api = "?UPSConnection"

    client.send(api + "\n")
    time.sleep(1)
    res = client.receive()

    # Example Response
    #
    # ?UPSConnection=0\n
    keys = res.split("=")
    if 1 < len(keys):
        status = keys[1]
        return status

def get_autoreboot(client):
    api = "?AutoReboot"

    client.send(api + "\n")
    time.sleep(1)
    res = client.receive()

    keys = res.split("=")
    if 1 < len(keys):
        status = keys[1]
        return status

def get_outletcount(client):
    api = "?OutletCount"

    client.send(api + "\n")
    time.sleep(1)
    res = client.receive()

    # Example Response
    #
    # ?OutletCount=6\n
    keys = res.split("=")
    if 1 < len(keys):
        status = keys[1]
        return status