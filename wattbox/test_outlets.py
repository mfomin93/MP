# # #
# Control API Wattbox Outlet Tests
#
# This test will run through the wattbox outlets performing all supported actions
#
# # #

import pytest
import time
import controlapi
import wattbox

@pytest.mark.parametrize("action", wattbox.OUTLET_ACTIONS)
def test_outlets(client, count, action):
    """ Outlets Test """

    print("Running Control API Outlet " + str(count) + " Action " + action + " Test")

    api = "!OutletSet=" + str(count) + "," + action

    client.send(api + "\n")
    time.sleep(1)
    res = client.receive()

    # Example Response
    #
    # !OutletSet=1,ON\n
    keys = res.split("=")
    if 1 < len(keys):
        val = keys[1]
        assert val != ""
    else:
        if res.rstrip() == controlapi.ERROR:
            pytest.fail("Error returned from call " + api)