from Crawler_Logic.Crawler import Crawler

def collect_papers(topic, max_papers=20, save_to_file=False):
    """Use the crawler to collect papers based on the topic."""
    crawler = Crawler(topic, max_papers, save_to_file)
    papers = crawler.run_all()

    if not papers:
        print("⚠️ No papers found by crawler.")
        return []

    print(f"✅\n Collected {len(papers)} papers from Crawler.")
    return papers