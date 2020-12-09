# # #
# Control API
#
# Contains helper functions and constants related to the control api
#
# # #

import time

WATTBOX_WIFI_MODELS = ["WB-150-IP-1B-2", "WB-150-IPW-1B-2", "WB-250-IPW-2"]
WATTBOX_VPS_MODELS = ["WB-800VPS-IPVM-18", "WB-800VPS-IPVM-12", "WB-800-IPVM-6", "WB-800-IPVM-12", "WB-800CH1U-IPVM-8", "WB-800CH2U-IPVM-12"]
MOIP_MODELS = ["B-900-MOIP-4K-CTRL"]

APIS = ["?Firmware", "?Hostname", "?ServiceTag", "?Model"]

PORT = 23

SUCCESS = "OK"
ERROR = "#Error"

GOOD_FIRMWARE_URLS = {
    "wattbox-vps": "https://embedded:TKP-2000@firmware.ovrc.com/files/wattbox-vps/upgrade_wattboxvps_2.0.1.2_20201118.bin",
    "wattbox-wifi": "https://embedded:TKP-2000@firmware.ovrc.com/files/wattbox-wifi/upgrade_wattboxwifi_2.0.1.2_20201118.bin",
    "moip-ctrl":  "https://embedded:TKP-2000@firmware.ovrc.com/files/moip/upgrade_moip_3.1.0.2_20201119.bin"
}

DUMMY_FIRMWARE_URLS = {
    "wattbox-vps": "https://embedded:TKP-2000@firmware.ovrc.com/files/wattbox-vps/upgrade_wattboxvps_2.0.1.3_20201118.bin",
    "wattbox-wifi": "https://embedded:TKP-2000@firmware.ovrc.com/files/wattbox-wifi/upgrade_wattboxwifi_2.0.1.3_20201118.bin",
    "moip-ctrl":  "https://embedded:TKP-2000@firmware.ovrc.com/files/moip/upgrade_moip_3.1.0.3_20201119.bin"
}

EMPTY_URL = ""
BAD_FIRMWARE = "https://embedded:TKP-2000@firmware.ovrc.com/files/bad_firmware/bad_firmware.bin"
NO_FILE = "https://embedded:TKP-2000@firmware.ovrc.com/files/non-existent-directory/non-existent-file.bin"

# #
# Helpers
# #

def login(client):
    client.send(client.username + "\n")
    time.sleep(0.1)
    client.receive()

    client.send(client.password + "\n")
    time.sleep(0.1)
    client.receive()

def get_model(client):
    api = "?Model"

    client.send(api + "\n")
    time.sleep(1)
    res = client.receive()

    # Example Response
    #
    # ?Model=OVRC-100-HUB\n
    keys = res.split("=")
    if 1 < len(keys):
        model = keys[1]
        return model

def get_version(client):
    api = "?Firmware"

    client.send(api + "\n")
    time.sleep(1)
    res = client.receive()

    # Example Response
    #
    # ?Firmware=6.0.0.0\n
    keys = res.split("=")
    if 1 < len(keys):
        version = keys[1]
        return version

def get_upgrade_url_from_model(model):

    for m in WATTBOX_VPS_MODELS:
        if model.rstrip() == m:
            return GOOD_FIRMWARE_URLS["wattbox-vps"]

    for m in WATTBOX_WIFI_MODELS:
        if model.rstrip() == m:
            return GOOD_FIRMWARE_URLS["wattbox-wifi"]

    for m in MOIP_MODELS:
        if model.rstrip() == m:
            return GOOD_FIRMWARE_URLS["moip-ctrl"]

    return ""

def get_dummy_upgrade_url_from_model(model):

    for m in WATTBOX_VPS_MODELS:
        if model.rstrip() == m:
            return DUMMY_FIRMWARE_URLS["wattbox-vps"]

    for m in WATTBOX_WIFI_MODELS:
        if model.rstrip() == m:
            return DUMMY_FIRMWARE_URLS["wattbox-wifi"]

    for m in MOIP_MODELS:
        if model.rstrip() == m:
            return DUMMY_FIRMWARE_URLS["moip-ctrl"]

    return ""