# # #
# Control API MoIP Resolution Tests
#
# This test will run through the MoIP resolution tests
#
# # #

import pytest
import time
import controlapi
import moip
import random

@pytest.mark.parametrize("resolution", moip.RESOLUTIONS)
def test_resolution(client, resolution):
    """ MoIP Resolution Test """

    count = moip.get_devicecount(client)
    devices = count.rstrip().split(",")

    receivers = int(devices[1])

    if receivers == 0:
        pytest.skip("No receivers to change resolution on")

    for rx in range(receivers):
        api = "!Resolution=" + str(rx+1) + "," + resolution

        client.send(api + "\n")
        time.sleep(1)
        res = client.receive()

        # Example
        #
        # !Resolution=1,1
        if res.rstrip() == controlapi.ERROR:
            pytest.fail("Error returned from call " + api)
