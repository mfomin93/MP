# # #
# Control API Wattbox Tests
#
# This test will run through the wattbox specific apis
#
# # #

import pytest
import time
import controlapi
import wattbox

@pytest.mark.parametrize("api", wattbox.APIS)
def test_wattboxapi(client, api):
    """Control Wattbox API Test"""

    print("Running Wattbox API Test: " + api)

    client.send(api + "\n")
    time.sleep(0.1)
    res = client.receive()

    # Example Response
    #
    # ?Model=OVRC-100-HUB\n
    keys = res.split("=")
    if 1 < len(keys):
        val = keys[1]
        assert val != ""
    else:
        if res.rstrip() == controlapi.ERROR:
            pytest.fail("Error returned from call " + api)