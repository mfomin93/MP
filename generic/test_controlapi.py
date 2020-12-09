# # #
# Control API Common Tests
#
# This test will run through the common apis every
# device running the control api will support
#
# # #

import pytest
import time
import controlapi

@pytest.mark.parametrize("api", controlapi.APIS)
def test_controlapi(client, api):
    print("Running Control API Test: " + api)

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