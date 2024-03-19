import yfinance as yf
import logging
from enums import *


"""
Portion of another project's module. Uses yahoo finance and pandas dataframes for the market environment.
"""

logger = logging.getLogger(__name__)


def _period_for_interval(interval: Interval) -> list:
    match interval:
        case Interval.ONE_MIN:
            return [Period.ONE_DAY, Period.FIVE_DAY, Period.MAX, Period.DT_SEVEN]
        case Interval.FIVE_MIN | Interval.FIFTEEN_MIN | Interval.THIRTY_MIN:
            return [Period.ONE_DAY, Period.FIVE_DAY, Period.ONE_MO, Period.MAX, Period.DT_FIFTY_NINE]
        case Interval.SIXTY_MIN | Interval.NINTY_MIN | Interval.ONE_HR:
            return [Period.ONE_DAY, Period.FIVE_DAY, Period.ONE_MO, Period.DT_SEVEN_HUNDRED_TWENTY_EIGHT]
        case Interval.ONE_DAY | Interval.FIVE_DAY:  # Warning: 5d period can have NaN for rows.
            return [Period.ONE_MO, Period.THREE_MO, Period.SIX_MO, Period.ONE_YR, Period.TWO_YR, Period.FIVE_YR,
                    Period.TEN_YR, Period.YTD, Period.MAX]
        case Interval.ONE_WEEk | Interval.ONE_MO:
            return [Period.SIX_MO, Period.ONE_YR, Period.TWO_YR, Period.FIVE_YR, Period.TEN_YR, Period.YTD, Period.MAX]
        case Interval.THREE_MO:
            return [Period.ONE_YR, Period.TWO_YR, Period.FIVE_YR, Period.TEN_YR, Period.YTD, Period.MAX]


def _check_period_to_interval(interval: Interval, period: Period | datetime.timedelta):
    allowed_periods = _period_for_interval(interval)

    if period == Period.MAX:
        return allowed_periods[-1]
    elif isinstance(period, datetime.timedelta):
        max_period = allowed_periods[-1]
        if isinstance(max_period, datetime.timedelta):  # Only the intraday intervals are limited
            if period > max_period:  # If the input period exceeds the max, the max is set instead.
                return max_period
            else:
                return period  # Timedelta given is less than max, return the given timedelta.
        else:
            return period  # Returns timedelta
    else:  # Enum.Period
        if period not in allowed_periods:
            new_period = allowed_periods[-1]  # Selects maximum period time for the given interval
            logger.warning(f"Period selected [{period}] not allowed for Interval: {interval.value}. "
                           f"Changed to period: [{new_period}]")
            return new_period
        else:
            return period


def request_market_data_for_ticker(ticker: str, interval: Interval, period: Period | datetime.timedelta,
                                   prepost=False) -> tuple:

    """
    Pull historical candlestick data for a ticker.
    """

    # Validate input parameters
    if not isinstance(ticker, str):
        raise ValueError("Ticker must be a string.")
    if not isinstance(interval, Interval):
        raise ValueError("Interval must be an instance of Interval enum.")
    if not isinstance(period, (Period, datetime.timedelta)):
        raise ValueError("Period must be an instance of Period enum or a datetime.timedelta.")

    # Check to see if inputs are correct
    period = _check_period_to_interval(interval, period)

    year_month_day_format = '%Y-%m-%d'
    if isinstance(period, datetime.timedelta):
        # Only if datetime is passed instead of Period.
        end = datetime.datetime.now()
        start = end - period
    elif isinstance(period.value, datetime.timedelta):
        end = datetime.datetime.now()
        start = end - period.value
    else:
        start = None
        end = None

    if start is not None and end is not None:
        start = start.strftime(year_month_day_format)
        end = end.strftime(year_month_day_format)

    df = yf.Ticker(ticker).history(start=start, end=end, interval=interval.value, period=period.value,
                                   auto_adjust=True, prepost=prepost)

    if len(df) == 0:
        logger.error(f"No stock data found for {ticker}. Returned None.")
        return ticker, None

    logger.debug(f'Market Data for {ticker} retrieved with time period: {period} | interval: {interval}')
    return ticker, df
