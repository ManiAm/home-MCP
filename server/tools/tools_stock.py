
import logging
from datetime import datetime, timezone

from apis.finnhubClient import Finnhub_REST_API_Client
from tools.decorator import include_as_tool

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)


class LLM_Stock():

    def __init__(self):

        self.fh_client = Finnhub_REST_API_Client(url="https://finnhub.io/api", api_ver="v1")


    @include_as_tool
    def symbol_lookup(self, query):
        """
        Search for best-matching company symbols.

        Parameters:
        - query (str): The search term (e.g., 'apple', 'tesla').
        """

        ok, output = self.fh_client.symbol_lookup(query)
        if not ok:
            return False, output

        if not output:
            return False, f"No matching symbols found for '{query}'."

        if not isinstance(output, list):
            return False, f"Unexpected output type: {type(output)}"

        top = output[0]

        output_str = (
            f"Top match for '{query}' is:\n"
            f"  Description: {top.get('description')}\n"
            f"  Symbol     : {top.get('symbol')}"
        )

        return True, output_str


    #################
    ##### Stock #####
    #################

    @include_as_tool
    def stock_symbols(self, exchange="US", currency="USD", max_items:int=5):
        """
        List supported stock symbols for a given exchange and optional currency filter.

        Parameters:
        - exchange (str): Exchange code (e.g., 'US', 'TO', 'HK').
        - currency (str, optional): Filter by currency (e.g., 'USD', 'CAD').
        - max_items (int, optional): Maximum number of stock symbols to display. Default is 5.
        """

        ok, output = self.fh_client.stock_symbols(exchange, currency)
        if not ok:
            return False, output

        if not isinstance(output, list):
            return False, f"Unexpected output type: {type(output)}"

        output_str = "Matched Stocks:"
        for info in output[:max_items]:
            output_str += (
                f"\n\n"
                f"  • Description      : {info.get('description', 'N/A')}\n"
                f"  • Symbol           : {info.get('symbol', 'N/A')}\n"
                f"  • Display Symbol   : {info.get('displaySymbol', 'N/A')}\n"
                f"  • Exchange (MIC)   : {info.get('mic', 'N/A')}\n"
                f"  • Currency         : {info.get('currency', 'N/A')}\n"
                f"  • Type             : {info.get('type', 'N/A')}\n"
                f"  • FIGI             : {info.get('figi', 'N/A')}\n"
                f"  • Share Class FIGI : {info.get('shareClassFIGI', 'N/A')}\n"
                f"  • ISIN             : {info.get('isin') or 'Not available'}\n"
            )

        print(output_str)

        return True, output_str


    @include_as_tool
    def market_status(self, exchange="US"):
        """
        Check if the specified market exchange is currently open or closed.

        Parameters:
        - exchange (str): Exchange code (e.g., 'US', 'TO', 'LSE').
        """

        ok, output = self.fh_client.market_status(exchange)
        if not ok:
            return False, output

        if not isinstance(output, dict):
            return False, f"Unexpected output type: {type(output)}"

        output_str = (
            f"Market status for {exchange}:\n"
            f"  isOpen : {output.get('isOpen')}\n"
            f"  timezone : {output.get('timezone')}"
        )

        return True, output_str


    @include_as_tool
    def market_holiday(self, exchange="US"):
        """
        List upcoming or recent market holidays for a given exchange.

        Parameters:
        - exchange (str): Exchange code (e.g., 'US', 'HK', 'LSE').
        """

        ok, output = self.fh_client.market_holiday(exchange)
        if not ok:
            return False, output

        if not isinstance(output, dict):
            return False, f"Unexpected output type: {type(output)}"

        data = output.get("data", [])

        holidays = [f"{h['eventName']}: {h['atDate']}" for h in data]
        output_str = "\n".join(holidays)
        return True, f"Upcoming market holidays for {exchange}:\n{output_str}"


    @include_as_tool
    def company_profile2(self, symbol):
        """
        Get general stock profile of a company including name, industry, market cap, country, and more.

        Parameters:
        - symbol (str): Stock ticker symbol (e.g., 'AAPL').
        """

        ok, output = self.fh_client.company_profile2(symbol)
        if not ok:
            return False, output

        if not isinstance(output, dict):
            return False, f"Unexpected output type: {type(output)}"

        output_str = (
            f"Company stock profile for symbol '{symbol}'\n"
            f"  Name        : {output.get('name')}\n"
            f"  Industry    : {output.get('finnhubIndustry')}\n"
            f"  Sector      : {output.get('industry', 'N/A')}\n"
            f"  Exchange    : {output.get('exchange')}\n"
            f"  Market Cap  : ${output.get('marketCapitalization', 'N/A')}B\n"
            f"  Shares Out  : {output.get('shareOutstanding', 'N/A')}M\n"
            f"  Country     : {output.get('country')}\n"
            f"  Currency    : {output.get('currency')}\n"
            f"  IPO Date    : {output.get('ipo')}\n"
            f"  Website     : {output.get('weburl')}\n"
            f"  Phone       : {output.get('phone')}"
        )

        return True, output_str


    @include_as_tool
    def company_peers(self, symbol):
        """
        List similar companies operating in the same sector and industry.

        Parameters:
        - symbol (str): Stock ticker symbol (e.g., 'MSFT').
        """

        ok, output = self.fh_client.company_peers(symbol)
        if not ok:
            return False, output

        if not isinstance(output, list):
            return False, f"Unexpected output type: {type(output)}"

        return True, f"Peers of {symbol}: {', '.join(output)}"


    @include_as_tool
    def company_basic_financials(self, symbol, metric="all"):
        """
        Summarize basic financial metrics like P/E ratio, profit margins, and 52-week high/low.

        Parameters:
        - symbol (str): Stock ticker symbol (e.g., 'GOOG').
        - metric (str): Financial metric to retrieve (e.g., 'valuation', 'margin', 'all').
        """

        ok, output = self.fh_client.company_basic_financials(symbol, metric)
        if not ok:
            return False, output

        if not isinstance(output, dict):
            return False, f"Unexpected output type: {type(output)}"

        metric = output.get("metric", {})

        output_str = (
            f"Financial highlights for {symbol}:\n"
            f"  • Market Cap: ${metric.get('marketCapitalization', 'N/A')}B\n"
            f"  • 52-Week High: ${metric.get('52WeekHigh', 'N/A')} on {metric.get('52WeekHighDate', 'N/A')}\n"
            f"  • 52-Week Low: ${metric.get('52WeekLow', 'N/A')} on {metric.get('52WeekLowDate', 'N/A')}\n"
            f"  • Dividend Yield (TTM): {metric.get('currentDividendYieldTTM', 'N/A')}%\n"
            f"  • EPS (TTM): {metric.get('epsTTM', 'N/A')}, P/E Ratio: {metric.get('peTTM', 'N/A')}\n"
            f"  • Operating Margin (TTM): {metric.get('operatingMarginTTM', 'N/A')}%\n"
            f"  • ROE (TTM): {metric.get('roeTTM', 'N/A')}%, ROA (TTM): {metric.get('roaTTM', 'N/A')}%\n"
            f"  • Revenue per Share (TTM): ${metric.get('revenuePerShareTTM', 'N/A')}\n"
            f"  • Book Value per Share (Quarterly): ${metric.get('bookValuePerShareQuarterly', 'N/A')}\n"
            f"  • Free Cash Flow per Share (TTM): ${metric.get('pfcfShareTTM', 'N/A')}\n"
            f"  • Cash Flow per Share (TTM): ${metric.get('cashFlowPerShareTTM', 'N/A')}"
        )

        return True, output_str


    @include_as_tool
    def stock_insider_transactions(self, symbol, from_date=None, to_date=None, max_items:int=10):
        """
        Show recent insider trading activity for a company, including executives buying or selling shares.

        Parameters:
        - symbol (str): Stock ticker symbol (e.g., 'NVDA').
        - from_date (str, optional): Start date in 'YYYY-MM-DD' format.
        - to_date (str, optional): End date in 'YYYY-MM-DD' format.
        - max_items (int, optional): Maximum number of transactions to display. Default is 10.
        """

        ok, data = self.fh_client.stock_insider_transactions(symbol, from_date, to_date)
        if not ok:
            return False, data

        if not data:
            return True, f"No insider transactions for {symbol}."

        if not isinstance(data, list):
            return False, f"Unexpected output type: {type(data)}"

        output_str = f"Insider transactions for {symbol}:\n"
        for txn in data[:max_items]:
            output_str += (
                f"  • {txn.get('name')} ({txn.get('transactionCode')}) "
                f"{txn.get('change')} shares on {txn.get('transactionDate')} "
                f"at ${txn.get('transactionPrice', 'N/A')}\n"
            )

        return True, output_str


    @include_as_tool
    def recommendation_trends(self, symbol):
        """
        Get current analyst recommendation trends for a company.

        Parameters:
        - symbol (str): Stock ticker symbol (e.g., 'AAPL').
        """

        ok, data = self.fh_client.recommendation_trends(symbol)
        if not ok:
            return False, data

        if not isinstance(data, list):
            return False, f"Unexpected output type: {type(data)}"

        output_str = ""
        for rec in data:
            output_str += (
                f"Analyst recommendation for {rec['symbol']} (as of {rec['period']}):\n"
                f"  • Strong Buy: {rec['strongBuy']}\n"
                f"  • Buy: {rec['buy']}\n"
                f"  • Hold: {rec['hold']}\n"
                f"  • Sell: {rec['sell']}\n"
                f"  • Strong Sell: {rec['strongSell']}\n"
            )

        return True, output_str


    ################
    ##### News #####
    ################

    @include_as_tool
    def market_news(self, category="general", min_id=0, max_items:int=3):
        """
        Summarize the latest general market news headlines.

        Parameters:
        - category (str): News category (e.g., 'general', 'forex', 'crypto').
        - min_id (int): Only return news with ID greater than this value.
        - max_items (int, optional): Maximum number of market news to display. Default is 3.
        """

        ok, data = self.fh_client.market_news(category, min_id)
        if not ok:
            return False, data

        if not isinstance(data, list):
            return False, f"Unexpected output type: {type(data)}"

        output_str = ""
        for article in data[:max_items]:
            dt = datetime.fromtimestamp(article['datetime'], tz=timezone.utc)
            dt_str = dt.strftime('%Y-%m-%d %H:%M UTC')
            output_str += (
                f"Headline : {article['headline']}\n"
                f"Summary  : {article['summary']}\n"
                f"Source   : {article['source']} | {dt_str}\n"
                f"Link     : {article['url']}\n\n"
            )

        return True, output_str


    @include_as_tool
    def company_news(self, symbol, from_date, to_date, max_items:int=3):
        """
        Summarize recent news articles related to a specific company.

        Parameters:
        - symbol (str): Stock ticker symbol (e.g., 'TSLA').
        - from_date (str): Start date in 'YYYY-MM-DD' format.
        - to_date (str): End date in 'YYYY-MM-DD' format.
        - max_items (int, optional): Maximum number of company news to display. Default is 3.
        """

        ok, data = self.fh_client.company_news(symbol, from_date, to_date)
        if not ok:
            return False, data

        if not data:
            return True, f"No news found for {symbol}."

        if not isinstance(data, list):
            return False, f"Unexpected output type: {type(data)}"

        output_str = ""
        for article in data[:max_items]:
            dt = datetime.fromtimestamp(article['datetime'], tz=timezone.utc)
            dt_str = dt.strftime('%Y-%m-%d %H:%M UTC')
            output_str += (
                f"Headline : {article['headline']}\n"
                f"Summary  : {article['summary']}\n"
                f"Source   : {article['source']} | {dt_str}\n"
                f"Link     : {article['url']}\n\n"
            )

        return True, output_str


    #################
    ##### Other #####
    #################

    @include_as_tool
    def ipo_calendar(self, from_date, to_date, max_items:int=3):
        """
        Get recent and upcoming IPO events in a date range.

        Parameters:
        - from_date (str): Start date in 'YYYY-MM-DD' format.
        - to_date (str): End date in 'YYYY-MM-DD' format.
        - max_items (int, optional): Maximum number of IPO to display. Default is 3.
        """

        ok, data = self.fh_client.ipo_calendar(from_date, to_date)
        if not ok:
            return False, data

        if not data:
            return False, "No upcoming IPOs."

        if not isinstance(data, list):
            return False, f"Unexpected output type: {type(data)}"

        output_str = ""

        for ipo in data[:max_items]:

            lines = []

            name = ipo.get("name")
            symbol = ipo.get("symbol")

            if name and symbol:
                lines.append(f"Name     : {name} ({symbol})")
            elif name:
                lines.append(f"Name     : {name}")
            elif symbol:
                lines.append(f"Symbol   : {symbol}")

            exchange = ipo.get("exchange")
            if exchange:
                lines.append(f"Exchange : {exchange}")

            date = ipo.get("date")
            if date:
                lines.append(f"Date     : {date}")

            shares = ipo.get("numberOfShares")
            price = ipo.get("price")

            if shares and isinstance(shares, (int, float)):
                shares_str = f"{shares:,}"
                if price:
                    lines.append(f"Shares   : {shares_str} @ ${price}")
                else:
                    lines.append(f"Shares   : {shares_str}")
            elif price:
                lines.append(f"Price    : ${price}")

            total_value = ipo.get("totalSharesValue")
            if total_value and isinstance(total_value, (int, float)):
                lines.append(f"Total    : ${total_value:,.0f}")

            status = ipo.get("status")
            if status:
                lines.append(f"Status   : {status.capitalize()}")

            output_str += "\n".join(lines) + "\n\n"

        return True, output_str


    @include_as_tool
    def company_quote(self, symbol):
        """
        Get the current stock price and related performance metrics.

        Parameters:
        - symbol (str): Stock ticker symbol (e.g., 'AMZN').
        """

        ok, output = self.fh_client.quote(symbol)
        if not ok:
            return False, output

        if not isinstance(output, dict):
            return False, f"Unexpected output type: {type(output)}"

        dt = datetime.fromtimestamp(output['t'], tz=timezone.utc)
        dt_str = dt.strftime('%Y-%m-%d %H:%M UTC')

        output_str = (
            f"{symbol} stock quote:\n"
            f"  Timestamp      : {dt_str}\n"
            f"  Current price  : ${output['c']}\n"
            f"  Change         : {output['d']} ({output['dp']}%)\n"
            f"  Open           : ${output['o']}\n"
            f"  High           : ${output['h']}\n"
            f"  Low            : ${output['l']}\n"
            f"  Previous close : ${output['pc']}"
        )

        return True, output_str


    ##################
    ##### Crypto #####
    ##################

    @include_as_tool
    def crypto_exchanges(self):
        """
        Retrieve a list of major cryptocurrency exchanges supported by the API.
        """

        ok, output = self.fh_client.crypto_exchanges()
        if not ok:
            return False, output

        if not isinstance(output, list):
            return False, f"Unexpected output type: {type(output)}"

        output_str = "\n".join(f"- {item}" for item in output)
        return True, f"Top supported crypto exchanges:\n{output_str}"


if __name__ == "__main__":

    stock_client = LLM_Stock()

    # status, output = stock_client.symbol_lookup("apple")

    # status, output = stock_client.stock_symbols()
    # status, output = stock_client.market_status()
    # status, output = stock_client.market_holiday()
    # status, output = stock_client.company_profile2("AAPL")
    # status, output = stock_client.company_peers("AAPL")
    # status, output = stock_client.company_basic_financials("AAPL")
    # status, output = stock_client.stock_insider_transactions("AAPL")
    # status, output = stock_client.recommendation_trends("AAPL")

    # status, output = stock_client.market_news()
    # status, output = stock_client.company_news("AAPL", from_date="2025-01-01", to_date="2025-03-01")

    # status, output = stock_client.ipo_calendar(from_date="2025-01-01", to_date="2025-04-01")
    # status, output = stock_client.quote("AAPL")

    # status, output = stock_client.crypto_exchanges()

    bla = 0
