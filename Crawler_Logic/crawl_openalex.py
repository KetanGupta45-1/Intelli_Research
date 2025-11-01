import requests
import urllib.parse
import time

def crawl_openalex(topic, max_papers=5):
    print(f"\n Searching OpenAlex for {topic}")
    encoded_topic = urllib.parse.quote(topic)
    api_url = f"https://api.openalex.org/works?filter=title.search:{encoded_topic}&per_page={max_papers}"
    headers = {
        'User-Agent': 'OpenAlexCrawler/1.0 (mailto:youremail@example.com)'
    }
    results = []

    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("⏰ Timeout: OpenAlex API took too long to respond.")
        return []
    except requests.exceptions.HTTPError as e:
        status = getattr(e.response, "status_code", "unknown")
        print(f"❌ HTTP Error {status} while fetching OpenAlex: {e}")
        return []
    except requests.exceptions.ConnectionError:
        print("🔌 Network error: Could not connect to OpenAlex.")
        return []
    except Exception as e:
        print(f"⚠️ Unexpected error while fetching OpenAlex: {e}")
        return []

    try:
        data = response.json()
    except Exception as e:
        print(f"⚠️ Failed to parse JSON from OpenAlex: {e}")
        return []

    works = data.get('results', [])
    if not works:
        print("⚠️ No papers found on OpenAlex (empty results).")
        return []

    for i, item in enumerate(works[:max_papers], 1):
        print(f"📄 OpenAlex: Processing {i}/{len(works)}")
        try:
            title = item.get('display_name') or item.get('title') or "N/A"
            authors = ', '.join(a.get('author', {}).get('display_name', '') for a in item.get('authorships', [])).strip() or "N/A"
            date = item.get('publication_date') or item.get('publication_year') or "N/A"

            # OpenAlex abstracts often come in inverted-index form or as 'abstract' field
            abstract = "N/A"
            abstract_idx = item.get('abstract_inverted_index')
            if abstract_idx:
                try:
                    # reconstruct from inverted index keys (best-effort)
                    abstract = " ".join(abstract_idx.keys()) if isinstance(abstract_idx, dict) else str(abstract_idx)
                except Exception:
                    abstract = "N/A"
            else:
                abstract = item.get('abstract', "N/A")

            paper_link = item.get('id', "N/A")
            pdf_link = item.get('primary_location', {}).get('landing_page_url', "N/A")

            results.append({
                'title': title,
                'authors': authors,
                'date': date,
                'abstract': abstract,
                'paper_link': paper_link
            })
            time.sleep(1)
        except KeyError as e:
            print(f"⚠️ Missing expected key in OpenAlex item: {e}")
        except Exception as e:
            print(f"⚠️ Error processing an OpenAlex item: {e}")
            continue

    print(f"✅ Collected {len(results)} papers from OpenAlex")
    return results
