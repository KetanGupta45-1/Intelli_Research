import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

def crawl_doaj(topic, max_papers=5):
    print(f"\n Searching DOAJ for {topic}")
    encoded_topic = urllib.parse.quote(topic)
    search_url = f"https://doaj.org/search/articles?ref=homepage&q={encoded_topic}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0 Safari/537.36'
    }
    results = []

    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("⏰ Timeout: DOAJ took too long to respond.")
        return []
    except requests.exceptions.HTTPError as e:
        status = getattr(e.response, "status_code", "unknown")
        print(f"❌ HTTP Error {status} while fetching DOAJ: {e}")
        return []
    except requests.exceptions.ConnectionError:
        print("🔌 Network error: Could not connect to DOAJ.")
        return []
    except Exception as e:
        print(f"⚠️ Unexpected error while fetching DOAJ: {e}")
        return []

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        papers = soup.find_all('div', class_='search-result') or soup.find_all('article', class_='search-result')
        if not papers:
            print("⚠️ No papers found on DOAJ (possible layout change).")
            return []

        for i, paper in enumerate(papers[:max_papers], 1):
            print(f"📄 DOAJ: Processing {i}/{len(papers)}")
            try:
                title_tag = paper.find('a', class_='title') or paper.find('h3')
                title = title_tag.get_text(strip=True) if title_tag else "N/A"

                link = title_tag['href'] if title_tag and title_tag.has_attr('href') else "N/A"
                if link != "N/A" and not link.startswith('http'):
                    link = urllib.parse.urljoin("https://doaj.org", link)

                authors_tag = paper.find('div', class_='authors')
                authors = authors_tag.get_text(strip=True) if authors_tag else "N/A"

                date = "N/A"
                abstract = "N/A"
                pdf_link = "N/A"

                results.append({
                    'title': title,
                    'authors': authors,
                    'date': date,
                    'abstract': abstract,
                    'paper_link': link
                })
                time.sleep(1)
            except KeyError as e:
                print(f"⚠️ Missing expected key in DOAJ paper: {e}")
            except Exception as e:
                print(f"⚠️ Error processing a DOAJ paper: {e}")
                continue

    except Exception as e:
        print(f"⚠️ Parsing error on DOAJ HTML: {e}")
        return []

    print(f"✅ Collected {len(results)} papers from DOAJ")
    return results
