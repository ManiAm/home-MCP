
# Author: Mani Amoozadeh
# Email: mani.amoozadeh2@gmail.com

import os
import sys
import getpass
import logging

from apis.rest_client import REST_API_Client
from apis.rate_limiter import RateLimiter, rate_limited

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)


class Finnhub_REST_API_Client(REST_API_Client):

    def __init__(self,
                 url=None,
                 api_ver=None,
                 base=None,
                 user=getpass.getuser(),
                 rate_limit=50,
                 rate_window=60):

        super().__init__(url, api_ver, base, user)

        self.API_KEY = os.getenv('FINNHUB_API_KEY', None)
        if not self.API_KEY:
            log.error("FINNHUB_API_KEY environment variable is missing!")
            sys.exit(1)

        self.rate_limiter = RateLimiter(
            key_prefix="finnhub_api",
            max_requests=rate_limit,
            interval_seconds=rate_window,
            user_id=user
        )


    @rate_limited
    def symbol_lookup(self, query):

        url = f"{self.baseurl}/search"
        params = {"q": query, "token": self.API_KEY}

        status, output = self.request("GET", url, params=params)
        if not status:
            return False, output

        if not isinstance(output, dict):
            return False, f"Unexpected output type: {type(output)}"

        result = output.get("result", [])

        return True, result


    #################
    ##### Stock #####
    #################

    @rate_limited
    def stock_symbols(self, exchange="US", currency="USD"):

        url = f"{self.baseurl}/stock/symbol"
        params = {"exchange": exchange, "currency": currency, "token": self.API_KEY}

        return self.request("GET", url, params=params)


    @rate_limited
    def market_status(self, exchange="US"):

        url = f"{self.baseurl}/stock/market-status"
        params = {"exchange": exchange, "token": self.API_KEY}

        return self.request("GET", url, params=params)


    @rate_limited
    def market_holiday(self, exchange="US"):

        url = f"{self.baseurl}/stock/market-holiday"
        params = {"exchange": exchange, "token": self.API_KEY}

        return self.request("GET", url, params=params)


    @rate_limited
    def company_profile2(self, symbol):

        url = f"{self.baseurl}/stock/profile2"
        params = {"symbol": symbol, "token": self.API_KEY}

        return self.request("GET", url, params=params)


    @rate_limited
    def company_peers(self, symbol):

        url = f"{self.baseurl}/stock/peers"
        params = {"symbol": symbol, "token": self.API_KEY}

        return self.request("GET", url, params=params)


    @rate_limited
    def company_basic_financials(self, symbol, metric="all"):

        url = f"{self.baseurl}/stock/metric"
        params = {"symbol": symbol, "metric": metric, "token": self.API_KEY}

        return self.request("GET", url, params=params)


    @rate_limited
    def stock_insider_transactions(self, symbol, from_date=None, to_date=None):

        url = f"{self.baseurl}/stock/insider-transactions"
        params = {"symbol": symbol, "from": from_date, "to": to_date, "token": self.API_KEY}

        status, output = self.request("GET", url, params=params)
        if not status:
            return False, output

        if not isinstance(output, dict):
            return False, f"Unexpected output type: {type(output)}"

        result = output.get("data", [])

        return True, result


    @rate_limited
    def financials_reported(self, symbol, freq="annual"):

        url = f"{self.baseurl}/stock/financials-reported"
        params = {"symbol": symbol, "freq": freq, "token": self.API_KEY}

        return self.request("GET", url, params=params)


    @rate_limited
    def filings(self, symbol, from_date=None, to_date=None):

        url = f"{self.baseurl}/stock/filings"
        params = {"symbol": symbol, "from_date": from_date, "to_date": to_date, "token": self.API_KEY}

        return self.request("GET", url, params=params)


    @rate_limited
    def recommendation_trends(self, symbol):

        url = f"{self.baseurl}/stock/recommendation"
        params = {"symbol": symbol, "token": self.API_KEY}

        return self.request("GET", url, params=params)


    ################
    ##### News #####
    ################

    @rate_limited
    def market_news(self, category="general", min_id=0):

        url = f"{self.baseurl}/news"
        params = {"category": category, "minId": min_id, "token": self.API_KEY}

        return self.request("GET", url, params=params)


    @rate_limited
    def company_news(self, symbol, from_date, to_date):

        url = f"{self.baseurl}/company-news"
        params = {"symbol": symbol, "from": from_date, "to": to_date, "token": self.API_KEY}

        return self.request("GET", url, params=params)


    #################
    ##### Other #####
    #################

    @rate_limited
    def ipo_calendar(self, from_date, to_date):

        url = f"{self.baseurl}/calendar/ipo"
        params = {"from": from_date, "to": to_date, "token": self.API_KEY}

        status, output = self.request("GET", url, params=params)
        if not status:
            return False, output

        if not isinstance(output, dict):
            return False, f"Unexpected output type: {type(output)}"

        result = output.get("ipoCalendar", [])

        return True, result


    @rate_limited
    def quote(self, symbol):

        url = f"{self.baseurl}/quote"
        params = {"symbol": symbol, "token": self.API_KEY}

        return self.request("GET", url, params=params)


    ##################
    ##### Crypto #####
    ##################

    @rate_limited
    def crypto_exchanges(self):

        url = f"{self.baseurl}/crypto/exchange"
        params = {"token": self.API_KEY}

        return self.request("GET", url, params=params)
