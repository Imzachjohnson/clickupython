import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from clickupy.helpers import timefuncs
import pytest


class TestTimeFuncs():

    @pytest.mark.timefuncs
    def test_fuzzy_time_to_unix(self):

        t = timefuncs.fuzzy_time_to_unix("december 1st")

        assert t == "1638345600000"    







