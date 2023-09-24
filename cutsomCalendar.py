from zipline.utils.memoize import lazyval
from pandas.tseries.offsets import CustomBusinessDay
from datetime import time
from pytz import timezone
import pandas as pd
from zipline.utils.calendar_utils import TradingCalendar


class twentyFourHourCalendar(TradingCalendar):
    """
    An exchange calendar for trading assets 24/7.

    Open Time: 12AM, UTC
    Close Time: 11:59PM, UTC
    """

    tz = timezone("UTC")

    @property
    def name(self):
        """
        The name of the exchange, which Zipline will look for
        when we run our algorithm and pass TFS to
        the --trading-calendar CLI flag.
        """
        return "TwentyFourHourCalendar"

    @property
    def open_times(self):
        """
        Method to specify the open times for each trading session.
        """
        return time(0, 0)

    @property
    def close_times(self):
        """
        Method to specify the close times for each trading session.
        """
        return time(23, 59)

    @lazyval
    def day(self):
        """
        The days on which our exchange will be open.
        """
        return CustomBusinessDay(weekmask="Mon Tue Wed Thu Fri Sat Sun")
