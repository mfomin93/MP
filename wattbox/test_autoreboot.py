# # #
# Control API Wattbox Auto Reboot Tests
#
# This test will run through the wattbox auto reboot performing all supported actions
#
# # #

import pytest
import time
import controlapi
import wattbox

@pytest.mark.parametrize("action", wattbox.OFF_ON_ACTIONS)
def test_autoreboot(client, action):
    """ Auto Reboot Test """

    print("Running Control API Auto Reboot Action " + action + " Test")

    api = "!AutoReboot=" + action

    client.send(api + "\n")
    time.sleep(1)
    res = client.receive()

    # Example Response
    #
    # !AutoReboot=0
    if res.rstrip() == controlapi.ERROR:
        pytest.fail("Error returned from call " + api)
    else:
        # Confirm setting
        setting = wattbox.get_autoreboot(client)

        assert setting.rstrip() == action