"""
Copyright 2017, MachineHeads
Author: Maria Sandrikova
Description: Tests for utils.py module
"""
import unittest
import json
import algo.tests.config as config 

from algo.utils import flatten_music_events

class TestUtils(unittest.TestCase):
    """
    Tests for utils.py module
    """

    def setUp(self):
        pass

    def test_flatten_music_events(self):
        """
        Tests utils.flatten_music_events function
        """
        with open(config.MARK_MUSIC_INFO_FILE, encoding="utf8") as json_file:
            music_info = json.load(json_file)
        new_events = flatten_music_events(music_info)
        self.assertTrue("type" in new_events[0])
        self.assertTrue("place" in new_events[0])
        self.assertTrue("name" in new_events[0])
        self.assertTrue("start_time" in new_events[0])
        self.assertTrue("id" in new_events[0])
        self.assertTrue("performer" in new_events[0])
        self.assertTrue("cover_url" in new_events[0])


if __name__ == '__main__':
    unittest.main()
