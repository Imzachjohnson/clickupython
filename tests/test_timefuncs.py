from clickupy.helpers import timefuncs
import pytest


class TestTimeFuncs():

    @pytest.mark.timefuncs
    def test_fuzzy_time_to_unix(self):

        t = timefuncs.fuzzy_time_to_unix("december first")
        t2 = timefuncs.fuzzy_time_to_unix("december 1st")

        assert t == "1638345600000"
        assert t2 == "1638345600000"


    @pytest.mark.timefuncs
    def test_fuzzy_time_to_seconds(self):

        t = timefuncs.fuzzy_time_to_seconds("5 hours")
        t2 = timefuncs.fuzzy_time_to_seconds("6 hours")

        assert t == 18000  
        assert t2 == 21600

