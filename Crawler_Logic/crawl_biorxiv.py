import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

def crawl_biorxiv(topic, max_papers=5):
    print(f"\n Searching BioRxiv for {topic}")
    encoded_topic = urllib.parse.quote(topic)
    search_url = f"https://www.biorxiv.org/search/{encoded_topic}%20numresults%3A{max_papers}%20sort%3Arelevance-rank"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    results = []

    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("⏰ Timeout: BioRxiv took too long to respond.")
        return []
    except requests.exceptions.HTTPError as e:
        status = getattr(e.response, "status_code", "unknown")
        print(f"❌ HTTP Error {status} while fetching BioRxiv: {e}")
        if status == 403:
            print("🔒 Access denied (403) — BioRxiv might be blocking automated requests.")
        return []
    except requests.exceptions.ConnectionError:
        print("🔌 Network error: Could not connect to BioRxiv.")
        return []
    except Exception as e:
        print(f"⚠️ Unexpected error while fetching BioRxiv: {e}")
        return []

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        papers = soup.find_all('div', class_='highwire-citation')
        if not papers:
            print("⚠️ No papers found on BioRxiv (possible layout change).")
            return []

        for i, paper in enumerate(papers[:max_papers], 1):
            print(f"📄 BioRxiv: Processing {i}/{len(papers)}")
            try:
                title_tag = paper.find('span', class_='highwire-citation-title')
                title = title_tag.get_text(strip=True) if title_tag else "N/A"

                authors_tag = paper.find('span', class_='highwire-citation-authors')
                authors = authors_tag.get_text(strip=True) if authors_tag else "N/A"

                date_tag = paper.find('span', class_='highwire-cite-metadata-date')
                date = date_tag.get_text(strip=True) if date_tag else "N/A"

                link_tag = paper.find('a', class_='highwire-cite-linked-title')
                paper_link = urllib.parse.urljoin("https://www.biorxiv.org", link_tag['href']) if link_tag and link_tag.has_attr('href') else "N/A"

                pdf_link = "N/A"
                if paper_link != "N/A" and 'abstract' in paper_link:
                    pdf_link = paper_link.replace('abstract', 'full.pdf')

                abstract = "N/A"
                if paper_link != "N/A":
                    try:
                        sub = requests.get(paper_link, headers=headers, timeout=10)
                        sub.raise_for_status()
                        sub_soup = BeautifulSoup(sub.content, 'html.parser')
                        abs_tag = sub_soup.find('div', class_='section abstract')
                        abstract = abs_tag.get_text(strip=True).replace('Abstract', '') if abs_tag else "N/A"
                    except requests.exceptions.Timeout:
                        print(f"⏰ Timeout when fetching abstract for '{title}'")
                    except requests.exceptions.HTTPError as e:
                        st = getattr(e.response, "status_code", "unknown")
                        print(f"❌ HTTP {st} when fetching abstract for '{title}'")
                    except Exception as e:
                        print(f"⚠️ Failed to fetch abstract for '{title}': {e}")
                        abstract = "N/A"

                results.append({
                    'title': title,
                    'authors': authors,
                    'date': date,
                    'abstract': abstract,
                    'paper_link': paper_link
                })
                time.sleep(1)
            except KeyError as e:
                print(f"⚠️ Missing expected key in BioRxiv paper: {e}")
            except Exception as e:
                print(f"⚠️ Error processing a BioRxiv paper: {e}")
                continue

    except Exception as e:
        print(f"⚠️ Parsing error on BioRxiv HTML: {e}")
        return []

    print(f"✅ Collected {len(results)} papers from BioRxiv")
    return results
