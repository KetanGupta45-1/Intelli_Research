import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

def crawl_dblp(topic, max_papers=5):
    print(f"\n Searching DBLP for {topic}")
    encoded_topic = urllib.parse.quote(topic)
    search_url = f"https://dblp.org/search?q={encoded_topic}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0 Safari/537.36'
    }
    results = []

    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("⏰ Timeout: DBLP took too long to respond.")
        return []
    except requests.exceptions.HTTPError as e:
        status = getattr(e.response, "status_code", "unknown")
        print(f"❌ HTTP Error {status} while fetching DBLP: {e}")
        return []
    except requests.exceptions.ConnectionError:
        print("🔌 Network error: Could not connect to DBLP.")
        return []
    except Exception as e:
        print(f"⚠️ Unexpected error while fetching DBLP: {e}")
        return []

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        papers = soup.find_all('li', class_='entry')
        if not papers:
            print("⚠️ No papers found on DBLP (possible layout change).")
            return []

        for i, paper in enumerate(papers[:max_papers], 1):
            print(f"📄 DBLP: Processing {i}/{len(papers)}")
            try:
                title_tag = paper.find('span', class_='title')
                title = title_tag.get_text(strip=True) if title_tag else "N/A"

                authors_tags = paper.find_all('span', itemprop='author')
                authors = ', '.join(a.get_text(strip=True) for a in authors_tags) if authors_tags else "N/A"

                year_tag = paper.find('span', class_='year')
                date = year_tag.get_text(strip=True) if year_tag else "N/A"

                link_tag = paper.find('a', href=True)
                paper_link = link_tag['href'] if link_tag else "N/A"

                # DBLP usually doesn't provide abstract on search result page
                abstract = "N/A"
                pdf_link = "N/A"

                results.append({
                    'title': title,
                    'authors': authors,
                    'date': date,
                    'abstract': abstract,
                    'paper_link': paper_link
                })
                time.sleep(1)
            except KeyError as e:
                print(f"⚠️ Missing expected key in DBLP paper: {e}")
            except Exception as e:
                print(f"⚠️ Error processing a DBLP paper: {e}")
                continue

    except Exception as e:
        print(f"⚠️ Parsing error on DBLP HTML: {e}")
        return []

    print(f"✅ Collected {len(results)} papers from DBLP")
    return results
