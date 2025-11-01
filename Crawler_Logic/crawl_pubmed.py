import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

def crawl_pubmed(topic, max_papers=5):
    print(f"\n Searching PubMed for {topic}")
    encoded_topic = urllib.parse.quote(topic)
    search_url = f"https://pubmed.ncbi.nlm.nih.gov/?term={encoded_topic}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    results = []

    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("⏰ Timeout: PubMed took too long to respond.")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error {response.status_code} while fetching PubMed: {e}")
        return []
    except requests.exceptions.ConnectionError:
        print("🔌 Network error: Could not connect to PubMed.")
        return []
    except Exception as e:
        print(f"⚠️ Unexpected error while fetching PubMed: {e}")
        return []

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        papers = soup.find_all('article', class_='full-docsum')
        if not papers:
            print("⚠️ No papers found on PubMed (possible layout change).")
            return []

        for i, paper in enumerate(papers[:max_papers], 1):
            print(f"📄 PubMed: Processing {i}/{len(papers)}")

            try:
                title_tag = paper.find('a', class_='docsum-title')
                title = title_tag.get_text(strip=True) if title_tag else "N/A"
                link = "https://pubmed.ncbi.nlm.nih.gov" + title_tag['href'] if title_tag else "N/A"
                authors = paper.find('span', class_='docsum-authors full-authors').get_text(strip=True) if paper.find('span', class_='docsum-authors full-authors') else "N/A"
                date = paper.find('span', class_='docsum-journal-citation full-journal-citation')
                date = date.get_text(strip=True).split('.')[0] if date else "N/A"

                abstract = "N/A"
                try:
                    sub = requests.get(link, headers=headers, timeout=10)
                    sub.raise_for_status()
                    sub_soup = BeautifulSoup(sub.text, 'html.parser')
                    abs_tag = sub_soup.find('div', class_='abstract-content selected')
                    abstract = abs_tag.get_text(strip=True) if abs_tag else "N/A"
                except Exception as e:
                    print(f"⚠️ Skipping abstract for '{title}' due to: {e}")

                results.append({
                    'title': title,
                    'authors': authors,
                    'date': date,
                    'abstract': abstract,
                    'paper_link': link
                })
                time.sleep(1)
            except KeyError as e:
                print(f"⚠️ Missing expected key in paper data: {e}")
            except Exception as e:
                print(f"⚠️ Error processing a paper: {e}")
                continue

    except Exception as e:
        print(f"⚠️ Parsing error on PubMed HTML: {e}")
        return []

    print(f"✅ Collected {len(results)} papers from PubMed")
    return results
