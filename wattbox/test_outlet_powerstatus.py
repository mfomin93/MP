# # #
# Control API Wattbox OutletPower Status Test
#
# This test will run through the wattbox outlet power status api
#
# # #

import pytest
import time
import controlapi
import wattbox

def test_powerstatus(client):
    """" Power Status Test"""

    is_vps = wattbox.vps_model_check(client)

    if not is_vps:
        pytest.skip("Power Status API not supported on this model")

    api = "?PowerStatus="

    client.send(api + "\n")
    time.sleep(1)
    res = client.receive()

    # Example Response
    #
    # ?PowerStatus=0.05,3.62,121.32,0\n
    keys = res.split("=")
    if 1 < len(keys):
        val = keys[1]
        assert val != ""
    else:
        if res.rstrip() == controlapi.ERROR:
            pytest.fail("Error returned from call " + api)

def test_outlets_powerstatus(client, count):
    """" Outlets Power Status Test"""

    is_vps = wattbox.vps_model_check(client)

    if not is_vps:
        pytest.skip("Power Status API not supported on this model")

    print("Querying Control API Outlet " + str(count) + " Power Status")

    api = "?OutletPowerStatus=" + str(count)

    client.send(api + "\n")
    time.sleep(1)
    res = client.receive()

    # Example Response
    #
    # ?OutletPowerStatus=1,0.00,0.00,119.34\n
    keys = res.split("=")
    if 1 < len(keys):

        # Confirm response
        assert keys[1] != ""

        # Split response into values
        values = keys[1].split(",")

        # Confirm outlet in response matches request
        assert values[0] == str(count)

    else:
        if res.rstrip() == controlapi.ERROR:
            pytest.fail("Error returned from call " + api)