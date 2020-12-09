# # #
# Control API Wattbox SDDP Tests
#
# This test will run through the wattbox auto reboot performing all supported actions
#
# # #

import pytest
import time
import controlapi
import wattbox

@pytest.mark.parametrize("action", wattbox.OFF_ON_ACTIONS)
def test_sddp(client, action):
    """ SDDP Test """

    print("Running Control API SDDP Action " + action + " Test")

    api = "!SetSDDP=" + action

    client.send(api + "\n")
    time.sleep(1)
    res = client.receive()

    if res.rstrip() == controlapi.ERROR:
        pytest.fail("Error returned from call " + api)
