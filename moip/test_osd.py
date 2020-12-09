# # #
# Control API MoIP OSD Tests
#
# This test will run through the MoIP OSD tests
#
# # #

import pytest
import time
import controlapi
import moip

def test_osd(client):
    """ MoIP OSD Test """

    count = moip.get_devicecount(client)
    devices = count.rstrip().split(",")

    receivers = int(devices[1])

    if receivers == 0:
        pytest.skip("No receivers to change osd on")

    for rx in range(receivers):
        api = "!OSD=" + str(rx+1) + "," + moip.OSD_TEST_TEXT

        client.send(api + "\n")
        time.sleep(1)
        res = client.receive()

        # Example
        #
        # !OSD=1,Test
        if res.rstrip() == controlapi.ERROR:
            pytest.fail("Error returned from call " + api)

def test_osd_clear(client):
    """ MoIP OSD Test """

    count = moip.get_devicecount(client)
    devices = count.rstrip().split(",")

    receivers = int(devices[1])

    if receivers == 0:
        pytest.skip("No receivers to change osd on")

    for rx in range(receivers):
        api = "!OSD=" + str(rx+1) + "," + moip.OSD_CLEAR_TEXT

        client.send(api + "\n")
        time.sleep(1)
        res = client.receive()

        # Example
        #
        # !OSD=1,CLEAR
        if res.rstrip() == controlapi.ERROR:
            pytest.fail("Error returned from call " + api)