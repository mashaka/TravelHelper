"""
Copyright 2017, MachineHeads
Author: Maria Sandrikova
Description: Entry point for package containing main trips generation routine
"""
from algo.utils import flatten_music_events

class UserInfo:
    """ Store information about a Facebookuser """

    def __init__(self, basic_info, music_info):
        self.music_events = flatten_music_events(music_info)

    def get_events(self):
        """ Return events based on user preferences  """
        return self.music_events

    def set_events(self, events):
        """ Set events"""
        self.music_events = events
