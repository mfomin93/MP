# # #
# Control API MoIP Scenes Tests
#
# This test will run through the MoIP scenes tests
#
# # #

import pytest
import time
import controlapi
import moip

def test_activatescenes(client):
    """ MoIP Scenes Test """

    scenes = moip.get_scenes(client)

    if scenes.rstrip() == "":
        pytest.skip("No scenes to activate")

    scenes = scenes.split(",")

    for scene in scenes:
        scene = scene.rstrip().strip("{}")

        api = "!ActivateScene=" + scene

        client.send(api + "\n")
        time.sleep(1)
        res = client.receive()

        # Example
        #
        # !ActivateScene=Test Scene
        if res.rstrip() == controlapi.ERROR:
            pytest.fail("Error returned from call " + api)