from clickupython.helpers import timefuncs
import pytest
from datetime import datetime
from clickupython import exceptions


class TestTimeFuncs:
    @pytest.mark.timefuncs
    def test_fuzzy_time_to_unix(self):

        from datetime import timezone

        dt = datetime(2022, 12, 1)
        unix_ts = dt.timestamp()
        final_timestamp = unix_ts * 1000

        t = timefuncs.fuzzy_time_to_unix("december 1 2022")

        assert t == str(int(final_timestamp))

        with pytest.raises(exceptions.ClickupClientError):
            t = timefuncs.fuzzy_time_to_unix("sdfsdfsdf")

    @pytest.mark.timefuncs
    def test_fuzzy_time_to_seconds(self):

        t = timefuncs.fuzzy_time_to_seconds("5 hours")
        t2 = timefuncs.fuzzy_time_to_seconds("6 hours")

        assert t == 18000
        assert t2 == 21600

        t = timefuncs.fuzzy_time_to_seconds("1632603494")
        assert t == "1632603494"
