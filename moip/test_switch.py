# # #
# Control API MoIP Switching Tests
#
# This test will run through the MoIP switching tests
#
# # #

import pytest
import time
import controlapi
import moip
import random

def test_disconnect(client):
    """ MoIP Disconnect Test """

    pytest.skip("Not support at this time")

    count = moip.get_devicecount(client)
    devices = count.rstrip().split(",")

    transmitters = int(devices[0])
    receivers = int(devices[1])

    if transmitters == 0:
        pytest.skip("No transmitters to switch")

    if receivers == 0:
        pytest.skip("No receivers to switch")

    for rx in range(receivers):
        api = "!Switch=" + "0" + "," + str(rx+1)

        client.send(api + "\n")
        time.sleep(1)
        res = client.receive()

        # Example
        #
        # !Switch=0,1
        if res.rstrip() == controlapi.ERROR:
            pytest.fail("Error returned from call " + api)

def test_switch(client):
    """ MoIP Switch Test """

    count = moip.get_devicecount(client)
    devices = count.rstrip().split(",")

    transmitters = int(devices[0])
    receivers = int(devices[1])

    if transmitters == 0:
        pytest.skip("No transmitters to switch")

    if receivers == 0:
        pytest.skip("No receivers to switch")

    rx_to_switch = str(random.randint(1, receivers))
    tx_to_switch = str(random.randint(1, transmitters))

    api = "!Switch=" + tx_to_switch + "," + rx_to_switch

    client.send(api + "\n")
    time.sleep(1)
    res = client.receive()

    # Example
    #
    # !Switch=1,1
    if res.rstrip() == controlapi.ERROR:
        pytest.fail("Error returned from call " + api)