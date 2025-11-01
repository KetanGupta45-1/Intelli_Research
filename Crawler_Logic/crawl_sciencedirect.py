import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

def crawl_sciencedirect(topic, max_papers=5):
    print(f"\n Searching ScienceDirect for {topic}")
    encoded_topic = urllib.parse.quote(topic)
    search_url = f"https://www.sciencedirect.com/search?qs={encoded_topic}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0 Safari/537.36'
    }
    results = []

    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("⏰ Timeout: ScienceDirect took too long to respond.")
        return []
    except requests.exceptions.HTTPError as e:
        status = getattr(e.response, "status_code", "unknown")
        print(f"❌ HTTP Error {status} while fetching ScienceDirect: {e}")
        return []
    except requests.exceptions.ConnectionError:
        print("🔌 Network error: Could not connect to ScienceDirect.")
        return []
    except Exception as e:
        print(f"⚠️ Unexpected error while fetching ScienceDirect: {e}")
        return []

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        papers = soup.find_all('div', class_='result-item-content')
        if not papers:
            print("⚠️ No papers found on ScienceDirect (possible JS rendering or layout change).")
            return []

        for i, paper in enumerate(papers[:max_papers], 1):
            print(f"📄 ScienceDirect: Processing {i}/{len(papers)}")
            try:
                title_tag = paper.find('h2') or paper.find('a', class_='result-list-title-link')
                title = title_tag.get_text(strip=True) if title_tag else "N/A"

                link_tag = paper.find('a', href=True)
                link = urllib.parse.urljoin("https://www.sciencedirect.com", link_tag['href']) if link_tag else "N/A"

                authors_tag = paper.find('span', class_='Authors')
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
                print(f"⚠️ Missing expected key in ScienceDirect paper: {e}")
            except Exception as e:
                print(f"⚠️ Error processing a ScienceDirect paper: {e}")
                continue

    except Exception as e:
        print(f"⚠️ Parsing error on ScienceDirect HTML: {e}")
        return []

    print(f"✅ Collected {len(results)} papers from ScienceDirect")
    return results
