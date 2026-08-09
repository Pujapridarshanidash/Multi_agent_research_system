
from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# TAVILY
# ============================================================

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information about a topic.
    Returns titles, URLs, and snippets from the search results.
    """

    results = tavily.search(
        query=query,
        max_results=5
    )

    formatted_results = []

    for result in results["results"]:
        formatted_results.append(
            f"""
Title: {result.get('title')}
URL: {result.get('url')}
Content: {result.get('content')}
"""
        )

    return "\n---\n".join(formatted_results)


# ============================================================
# BEAUTIFULSOUP
# ============================================================


@tool
def scrape_url(url: str) -> str:
    """Scrape a webpage and extract its title and clean text content."""

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Get title
        title = soup.title.get_text(strip=True) if soup.title else "No title"

        # Remove unwanted elements
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()

        # Extract paragraphs
        paragraphs = []

        for p in soup.find_all("p"):
            text = p.get_text(" ", strip=True)

            if text:
                paragraphs.append(text)

        content = "\n\n".join(paragraphs)

        return f"""
TITLE:
{title}

URL:
{url}

CONTENT:
{content[:5000]}
"""

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
    
if __name__ == "__main__":

    print("\n===== BEAUTIFULSOUP TEST =====")
    result = scrape_url.invoke(
    "https://en.wikipedia.org/wiki/Artificial_intelligence"
)

    print(result)

