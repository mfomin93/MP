# # #
# Control API MoIP Tests
#
# This test will run through the MoIP specific apis
#
# # #

import pytest
import time
import controlapi
import moip

@pytest.mark.parametrize("api", moip.APIS)
def test_moipapi(client, api):
    """Control MoIP API Test"""

    print("Running MoIP API Test: " + api)

    client.send(api + "\n")
    time.sleep(0.1)
    res = client.receive()

    keys = res.split("=")
    if 1 < len(keys):
        val = keys[1]
        assert val != ""
    else:
        if res.rstrip() == controlapi.ERROR:
            pytest.fail("Error returned from call " + api)