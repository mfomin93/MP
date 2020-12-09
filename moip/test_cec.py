# # #
# Control API MoIP CEC Tests
#
# This test will run through the MoIP CEC tests
#
# # #

import pytest
import time
import controlapi
import moip

@pytest.mark.parametrize("mode", moip.CEC_MODES)
def test_cec(client, mode):
    """ MoIP CEC Test """

    count = moip.get_devicecount(client)
    devices = count.rstrip().split(",")

    receivers = int(devices[1])

    if receivers == 0:
        pytest.skip("No receivers to change osd on")

    for rx in range(receivers):
        api = "!CEC=" + str(rx+1) + "," + mode

        client.send(api + "\n")
        time.sleep(1)
        res = client.receive()

        # Example
        #
        # !CEC=1,0
        if res.rstrip() == controlapi.ERROR:
            pytest.fail("Error returned from call " + api)