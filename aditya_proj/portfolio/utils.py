import base64
import io

import matplotlib.pyplot as plt
import requests_cache
import yfinance as yf
from pandas_datareader import data as pdr
from pyrate_limiter import Duration, Limiter, RequestRate
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass


session = CachedLimiterSession(
    limiter=Limiter(
        RequestRate(2, Duration.SECOND * 5)
    ),  # max 2 requests per 5 seconds
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache("yfinance.cache"),
)


def data_fun(stock):
    msft = yf.Ticker("MSFT")

    msft.info

    hist = msft.history(period="1mo")
    msft.history_metadata

    msft.actions
    msft.dividends
    msft.splits
    msft.capital_gains

    # show share count
    msft.get_shares_full(start="2024-01-01", end=None)

    # show financials:
    # - income statement
    msft.income_stmt
    msft.quarterly_income_stmt
    # - balance sheet
    msft.balance_sheet
    msft.quarterly_balance_sheet
    # - cash flow statement
    msft.cashflow
    msft.quarterly_cashflow
    # see `Ticker.get_income_stmt()` for more options

    # show holders
    msft.major_holders
    msft.institutional_holders
    msft.mutualfund_holders
    msft.insider_transactions
    msft.insider_purchases
    msft.insider_roster_holders

    msft.recommendations
    msft.recommendations_summary
    msft.upgrades_downgrades

    msft.earnings_dates

    msft.isin

    msft.options

    msft.news
    opt = msft.option_chain("2024-02-16")

    msft = yf.Ticker("MSFT")

    msft.get_actions(proxy="PROXY_SERVER")
    msft.get_dividends(proxy="PROXY_SERVER")
    msft.get_splits(proxy="PROXY_SERVER")
    msft.get_capital_gains(proxy="PROXY_SERVER")
    msft.get_balance_sheet(proxy="PROXY_SERVER")
    msft.get_cashflow(proxy="PROXY_SERVER")

    tickers = yf.Tickers("msft aapl goog")

    tickers.tickers["MSFT"].info
    tickers.tickers["AAPL"].history(period="1mo")
    tickers.tickers["GOOG"].actions

    data = yf.download("SPY AAPL", period="1mo")

    session = requests_cache.CachedSession("yfinance.cache")
    session.headers["User-agent"] = "my-program/1.0"
    ticker = yf.Ticker("msft", session=session)
    # The scraped response will be stored in the cache
    ticker.actions

    yf.pdr_override()  # <== that's all it takes :-)

    # download dataframe
    data = pdr.get_data_yahoo(stock, start="2024-01-01", end="2024-02-01")

    fig = plt.figure(figsize=(10, 6))
    plt.plot(data.index, data["Close"], label="Close Price", color="blue")

    # Adding titles and labels
    plt.title("SPY Close Price (Jan-Feb 2024)")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()

    # Rotating x-axis labels for better readability
    plt.xticks(rotation=45)

    # Displaying the plot
    plt.grid(True)
    plt.tight_layout()

    flike = io.BytesIO()
    fig.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    return b64
