import requests
from bs4 import BeautifulSoup


def extract_news(company_name):
    search_query = f"{company_name} news"
    url = f"https://www.bing.com/search?q={search_query}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch news articles.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    for item in soup.find_all('li', {'class': 'b_algo'}):
        try:
            title_tag = item.find('a')
            title = title_tag.text
            link = title_tag['href']

            # Check if the link is accessible and valid (non-JS)
            link_response = requests.head(link, allow_redirects=True)
            if link_response.status_code != 200:
                continue

            # Extract summary if available
            summary_tag = item.find('p')
            summary = summary_tag.text if summary_tag else "No summary available"

            # Append valid results
            results.append({"title": title, "link": link, "summary": summary})

            # Stop after getting 10 valid articles
            if len(results) == 10:
                break
        except Exception as e:
            print(f"Error processing an article: {e}")
            continue

    return results
