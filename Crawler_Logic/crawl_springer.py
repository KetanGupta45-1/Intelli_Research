import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

def crawl_springer(topic, max_papers=5):
    print(f"\n Searching Springer for {topic}")
    encoded_topic = urllib.parse.quote(topic)
    search_url = f"https://link.springer.com/search?query={encoded_topic}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0 Safari/537.36'
    }
    results = []

    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("⏰ Timeout: Springer took too long to respond.")
        return []
    except requests.exceptions.HTTPError as e:
        status = getattr(e.response, "status_code", "unknown")
        print(f"❌ HTTP Error {status} while fetching Springer: {e}")
        return []
    except requests.exceptions.ConnectionError:
        print("🔌 Network error: Could not connect to Springer.")
        return []
    except Exception as e:
        print(f"⚠️ Unexpected error while fetching Springer: {e}")
        return []

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        papers = soup.find_all('li', class_='has-cover')
        if not papers:
            print("⚠️ No papers found on Springer (possible layout change).")
            return []

        for i, paper in enumerate(papers[:max_papers], 1):
            print(f"📄 Springer: Processing {i}/{len(papers)}")
            try:
                title_tag = paper.find('h2') or paper.find('h3')
                title = title_tag.get_text(strip=True) if title_tag else "N/A"

                link_tag = title_tag.find('a') if title_tag else None
                link = urllib.parse.urljoin("https://link.springer.com", link_tag['href']) if link_tag and link_tag.has_attr('href') else "N/A"

                authors_tag = paper.find('span', class_='authors') or paper.find('span', class_='authors__name')
                authors = authors_tag.get_text(strip=True) if authors_tag else "N/A"

                date_tag = paper.find('span', class_='year')
                date = date_tag.get_text(strip=True) if date_tag else "N/A"

                abstract = "N/A"
                pdf_link = "N/A"

                # Try to fetch abstract page if link available
                if link != "N/A":
                    try:
                        sub = requests.get(link, headers=headers, timeout=10)
                        sub.raise_for_status()
                        sub_soup = BeautifulSoup(sub.content, 'html.parser')
                        abs_tag = sub_soup.find('section', class_='Abstract') or sub_soup.find('section', class_='c-article-section__content')
                        abstract = abs_tag.get_text(strip=True).replace('Abstract', '') if abs_tag else "N/A"
                    except Exception as e:
                        print(f"⚠️ Skipping abstract fetch for '{title}': {e}")

                results.append({
                    'title': title,
                    'authors': authors,
                    'date': date,
                    'abstract': abstract,
                    'paper_link': link
                })
                time.sleep(1)
            except KeyError as e:
                print(f"⚠️ Missing expected key in Springer paper: {e}")
            except Exception as e:
                print(f"⚠️ Error processing a Springer paper: {e}")
                continue

    except Exception as e:
        print(f"⚠️ Parsing error on Springer HTML: {e}")
        return []

    print(f"✅ Collected {len(results)} papers from Springer")
    return results
