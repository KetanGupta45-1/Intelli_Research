import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

def crawl_ieee(topic, max_papers=5):
    print(f"\n Searching IEEE Xplore for {topic}")
    encoded_topic = urllib.parse.quote(topic)
    search_url = f"https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText={encoded_topic}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0 Safari/537.36'
    }
    results = []

    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("⏰ Timeout: IEEE Xplore took too long to respond.")
        return []
    except requests.exceptions.HTTPError as e:
        status = getattr(e.response, "status_code", "unknown")
        print(f"❌ HTTP Error {status} while fetching IEEE: {e}")
        return []
    except requests.exceptions.ConnectionError:
        print("🔌 Network error: Could not connect to IEEE Xplore.")
        return []
    except Exception as e:
        print(f"⚠️ Unexpected error while fetching IEEE Xplore: {e}")
        return []

    try:
        # NOTE: IEEE often requires JS. Attempt the static page; if empty, inform user.
        soup = BeautifulSoup(response.content, 'html.parser')
        papers = soup.find_all('div', class_='List-results-items') or soup.find_all('div', class_='List-results-item')
        if not papers:
            print("⚠️ No papers found on IEEE (site may require JS/API access).")
            return []

        for i, paper in enumerate(papers[:max_papers], 1):
            print(f"📄 IEEE: Processing {i}/{len(papers)}")
            try:
                title_tag = paper.find('h2') or paper.find('h3')
                title = title_tag.get_text(strip=True) if title_tag else "N/A"

                link_tag = title_tag.find('a') if title_tag else None
                link = urllib.parse.urljoin("https://ieeexplore.ieee.org", link_tag['href']) if link_tag and link_tag.has_attr('href') else "N/A"

                authors = "N/A"
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
                print(f"⚠️ Missing expected key in IEEE paper: {e}")
            except Exception as e:
                print(f"⚠️ Error processing an IEEE paper: {e}")
                continue

    except Exception as e:
        print(f"⚠️ Parsing error on IEEE HTML: {e}")
        return []

    print(f"✅ Collected {len(results)} papers from IEEE")
    return results
