"""
Copyright 2017, MachineHeads
Author: Maria Sandrikova
Description: Tests for generator.py module
"""
import unittest
import os
import logging
from logging import handlers
import sys
import json
import algo.tests.config as config

from algo import generate_trips

class TestGeneration(unittest.TestCase):
    """
    Tests for generator.py module
    """
    @staticmethod
    def set_up_logs():
        """ Set up logging """
        if not os.path.exists(config.OUTPUT_DIR):
            os.makedirs(config.OUTPUT_DIR)
        logger = logging.getLogger('')
        logger.setLevel(logging.INFO)
        log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)
        file_handler = handlers.RotatingFileHandler(
            config.LOG_FILE,
            backupCount=7
        )
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

    def test_generate_trips(self):
        """
        Tests only correctness of an output json for generate.generate_trips function
        """
        TestGeneration.set_up_logs()
        with open(config.MARK_MUSIC_INFO_FILE, encoding="utf8") as json_file:
            music_info = json.load(json_file)
        trips = generate_trips([], music_info)
        with open(config.TRIPS_OUTPUT_FILE, 'w') as outfile:
            json.dump(trips, outfile, indent=4)


if __name__ == '__main__':
    unittest.main()
