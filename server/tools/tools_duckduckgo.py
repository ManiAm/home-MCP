
from duckduckgo_search import DDGS
from tools.decorator import include_as_tool

class DuckDuckGoSearch:

    @include_as_tool
    def web_search(self, query: str):
        """
        Perform a web search using DuckDuckGo and return a summary of results.
        Use this tool for general knowledge or financial facts not known internally.

        Parameters:
            query (str): The search query string.
        """

        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=5)
            if not results:
                return False, "No results found."

            return True, self.format_ddg_results(results)


    def format_ddg_results(self, results):

        formatted = []

        for i, item in enumerate(results, start=1):
            title = item.get('title', 'No Title')
            url = item.get('href', 'No URL')
            snippet = item.get('body', '')
            entry = f"{i}. {title}\nURL: {url}\nSnippet: {snippet.strip()}"
            formatted.append(entry)

        return "\n\n".join(formatted)


if __name__ == "__main__":

    search_client = DuckDuckGoSearch()
    result_str = search_client.search("who is bill gates?")
