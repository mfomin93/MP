# # #
# Control API MoIP Tests
#
# Contains helper functions and constants related to the MoIP control api
#
# # #

import time
import controlapi

APIS = ["?Receivers", "?Devices", "?Name=0", "?Name=1"]
RESOLUTIONS = ["0", "1", "2", "3", "4"]
CEC_MODES = ["0", "1"]

OSD_TEST_TEXT = "Automated Tests are Awesome!!!"
OSD_CLEAR_TEXT = "CLEAR"

IR_PRONTO_CODE = ("0000 0066 0000 000d 0061 0019 0030 0019 0019 0019 0030 0019 0019 0019 0019 0019 0030"
                  "0019 0030 0019 0030 0019 0019 0019 0019 0019 0019 0019 0019 0400")

# #
# Helpers
# #
def get_devicecount(client):
    api = "?Devices"

    client.send(api + "\n")
    time.sleep(1)
    res = client.receive()

    # Example Response
    #
    # ?Devices=3,3\n
    keys = res.split("=")
    if 1 < len(keys):
        devices = keys[1]
        return devices

def get_scenes(client):
    api = "?Scenes"

    client.send(api + "\n")
    time.sleep(1)
    res = client.receive()

    # Example Response
    #
    # ?Scenes={Test Scene}\n
    keys = res.split("=")
    if 1 < len(keys):
        scenes = keys[1]
        return scenes