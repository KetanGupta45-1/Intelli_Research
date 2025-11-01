import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

def crawl_arxiv(topic, max_papers=5):
    print(f"\n Searching arXiv for {topic}")
    encoded_topic = urllib.parse.quote(topic)
    search_url = f"https://arxiv.org/search/?query={encoded_topic}&searchtype=all"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    results = []

    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()

    except requests.exceptions.Timeout:
        print("⏰ Timeout: arXiv took too long to respond.")
        return []
    
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error {response.status_code} while fetching arXiv: {e}")
        return []
    
    except requests.exceptions.ConnectionError:
        print("🔌 Network error: Could not connect to arXiv.")
        return []
    
    except Exception as e:
        print(f"⚠️ Unexpected error while fetching arXiv: {e}")
        return []

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        papers = soup.find_all('li', class_='arxiv-result')
        if not papers:
            print("⚠️ No papers found on arXiv (possible layout change).")
            return []

        for i, paper in enumerate(papers[:max_papers], 1):
            print(f"📄 arXiv: Processing {i}/{len(papers)}")

            try:
                title_tag = paper.find('p', class_='title is-5 mathjax')
                title = title_tag.get_text(strip=True) if title_tag else "N/A"

                link_tag = paper.find('p', class_='list-title is-inline-block')
                link = link_tag.find('a')['href'] if link_tag and link_tag.find('a') else "N/A"

                authors_tag = paper.find('p', class_='authors')
                authors = authors_tag.get_text(strip=True).replace('Authors:', '') if authors_tag else "N/A"

                date_tag = paper.find('p', class_='is-size-7')
                date = date_tag.get_text(strip=True) if date_tag else "N/A"

                abstract_tag = paper.find('span', class_='abstract-full has-text-grey-dark mathjax')
                abstract = abstract_tag.get_text(strip=True).replace('△ Less', '') if abstract_tag else "N/A"

                pdf_link_tag = paper.find('a', string='pdf')
                pdf_link = pdf_link_tag['href'] if pdf_link_tag else "N/A"
                if pdf_link != "N/A" and not pdf_link.startswith('http'):
                    pdf_link = "https://arxiv.org" + pdf_link

                results.append({
                    'title': title,
                    'authors': authors,
                    'date': date,
                    'abstract': abstract,
                    'paper_link': link
                })
                time.sleep(1)
            except Exception as e:
                print(f"⚠️ Error processing a paper: {e}")
                continue

    except Exception as e:
        print(f"⚠️ Parsing error on arXiv HTML: {e}")
        return []

    print(f"✅ Collected {len(results)} papers from arXiv")
    return results
