# # #
# Control API MoIP IR Tests
#
# This test will run through the MoIP IR tests
#
# # #

import pytest
import time
import controlapi
import moip

def test_ir(client):
    """ MoIP IR Test """

    count = moip.get_devicecount(client)
    devices = count.rstrip().split(",")

    transmitters = int(devices[0])
    receivers = int(devices[1])

    if transmitters == 0:
        pytest.skip("No transmitters to send ir code to")

    if receivers == 0:
        pytest.skip("No receivers to send ir code to")

    for rx in range(receivers):
        api = "!IR=0," + str(rx+1) + "," + moip.IR_PRONTO_CODE

        client.send(api + "\n")
        time.sleep(1)
        res = client.receive()

        # Example
        #
        # !IR=0,1,0000 1111 2222
        if res.rstrip() == controlapi.ERROR:
            pytest.fail("Error returned from call " + api)

    for tx in range(transmitters):
        api = "!IR=1," + str(tx+1) + "," + moip.IR_PRONTO_CODE

        client.send(api + "\n")
        time.sleep(1)
        res = client.receive()

        # Example
        #
        # !IR=1,1,0000 1111 2222
        if res.rstrip() == controlapi.ERROR:
            pytest.fail("Error returned from call " + api)