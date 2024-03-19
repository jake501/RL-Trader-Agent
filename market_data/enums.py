from base_enum import BaseEnum
import datetime


class Interval(BaseEnum):
    """
    The bar length, or 'interval' of OHLC stock data.
    """
    ONE_MIN = '1m'
    FIVE_MIN = '5m'
    FIFTEEN_MIN = '15m'
    THIRTY_MIN = '30m'
    SIXTY_MIN = '60m'
    NINTY_MIN = '90m'
    ONE_HR = '1h'
    ONE_DAY = '1d'
    FIVE_DAY = '5d'
    ONE_WEEk = '1wk'
    ONE_MO = '1mo'
    THREE_MO = '3mo'


class Period(BaseEnum):
    """
    The length of time that OHLC stock data extends back.
    """
    ONE_DAY = '1d'
    FIVE_DAY = '5d'
    ONE_MO = '1mo'
    THREE_MO = '3mo'
    SIX_MO = '6mo'
    ONE_YR = '1y'
    TWO_YR = '2y'
    FIVE_YR = '5y'
    TEN_YR = '10y'
    YTD = 'ytd'
    MAX = 'max'
    DT_SEVEN = datetime.timedelta(7)
    DT_FIFTY_NINE = datetime.timedelta(59)
    DT_SEVEN_HUNDRED_TWENTY_EIGHT = datetime.timedelta(728)  # Max is 730 but messes up when requesting data at night
