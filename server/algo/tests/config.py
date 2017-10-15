"""
Copyright 2017, MachineHeads
Author: Maria Sandrikova
Description: Config for trips generation tests
"""
import os

WORKING_DIR = os.path.dirname(__file__)

DATA_DIR = os.path.join(WORKING_DIR, 'data')

MARK_BASIC_INFO_FILE = os.path.join(DATA_DIR, 'mark_basic_info.json')
MARK_MUSIC_INFO_FILE = os.path.join(DATA_DIR, 'mark_music_info.json')

OUTPUT_DIR = os.path.join(WORKING_DIR, 'output')
LOG_FILE = os.path.join(OUTPUT_DIR, 'log_file.log')
TRIPS_OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'mark_trips.json')
