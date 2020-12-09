# # #
# Control API Wattbox UPS Tests
#
# This test will run through the wattbox specific apis related to UPS
#
# # #

import pytest
import time
import controlapi
import wattbox

def test_ups(client):
    """ UPS Test """

    is_vps = wattbox.vps_model_check(client)

    if not is_vps:
        pytest.skip("UPS API not supported on this model")

    # Check if UPS is actually connected
    conn = wattbox.get_upsconnection(client)
    assert conn != ""

    if conn.rstrip() == "0":
        api = "?UPSStatus"

        client.send(api + "\n")
        time.sleep(1)
        res = client.receive()

        # Example Response
        #
        # ?UPSStatus=0,0,Good,False,0,False,False\n
        keys = res.split("=")
        if 1 < len(keys):
            val = keys[1]
            assert val != ""
        else:
            if res.rstrip() == controlapi.ERROR:
                pytest.fail("Error returned from call " + api)