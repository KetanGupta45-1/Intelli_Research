from Crawler_Logic.crawl_arxiv import crawl_arxiv
from Crawler_Logic.crawl_biorxiv import crawl_biorxiv
from Crawler_Logic.crawl_dblp import crawl_dblp
from Crawler_Logic.crawl_doaj import crawl_doaj
from Crawler_Logic.crawl_openalex import crawl_openalex
from Crawler_Logic.crawl_ieee import crawl_ieee
from Crawler_Logic.crawl_pubmed import crawl_pubmed
from Crawler_Logic.crawl_sciencedirect import crawl_sciencedirect
from Crawler_Logic.crawl_springer import crawl_springer
import os


class Crawler:
    def __init__(self, topic, max_papers, save_to_file):
        self.topic = self.normalize_topic(topic)
        self.max_papers = max_papers
        self.save_to_file = save_to_file

        self.arxiv_res = []
        self.bioxiv_res = []
        self.dblp_res = []
        self.doaj_res = []
        self.openalex_res = []
        self.ieee_res = []
        self.pubmed_res = []
        self.sciencedirect_res = []
        self.springer_res = []
        self.all_papers = []

    def normalize_topic(self, topic):
        topic = topic.strip().replace("_", " ")
        return " ".join(word.capitalize() for word in topic.split())

    def safe_run(self, func, name):
        try:
            print(f"Collecting {name} Papers")
            res = func(topic=self.topic, max_papers=self.max_papers)
            if not res:
                print(f"No Papers Collected from {name}")
            else:
                print(f"Collected {len(res)} papers from {name}")
            return res
        except Exception as e:
            print(f"❌ Cannot collect papers from {name}: {e}")
            return []

    def run_all(self):
        print(f"\n🚀 Starting Crawl for Topic: {self.topic}\n")

        self.arxiv_res = self.safe_run(crawl_arxiv, "Arxiv")
        self.bioxiv_res = self.safe_run(crawl_biorxiv, "BioRxiv")
        self.dblp_res = self.safe_run(crawl_dblp, "DBLP")
        self.doaj_res = self.safe_run(crawl_doaj, "DOAJ")
        self.openalex_res = self.safe_run(crawl_openalex, "OpenAlex")
        self.ieee_res = self.safe_run(crawl_ieee, "IEEE")
        self.pubmed_res = self.safe_run(crawl_pubmed, "PubMed")
        self.sciencedirect_res = self.safe_run(crawl_sciencedirect, "ScienceDirect")
        self.springer_res = self.safe_run(crawl_springer, "Springer")

        self.all_papers = (
            self.arxiv_res +
            self.bioxiv_res +
            self.dblp_res +
            self.doaj_res +
            self.openalex_res +
            self.ieee_res +
            self.pubmed_res +
            self.sciencedirect_res +
            self.springer_res
        )

        if self.save_to_file and self.all_papers:
            filename = f"research_{self.topic.replace(' ', '_').lower()}.txt"

            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Research Papers on: {self.topic}\n")
                f.write(f"Total Collected: {len(self.all_papers)}\n")
                f.write("=" * 80 + "\n\n")

                for idx, paper in enumerate(self.all_papers, 1):
                    f.write(f"Paper #{idx}\n")
                    f.write(f"Title: {paper.get('title', 'N/A')}\n")
                    f.write(f"Authors: {paper.get('authors', 'N/A')}\n")
                    f.write(f"Publication Date: {paper.get('date', 'N/A')}\n")
                    f.write(f"Abstract: {paper.get('abstract', 'N/A')}\n")
                    f.write("-" * 80 + "\n\n")

            print(f"\n📦 Number of Papers -> {len(self.all_papers)}")
            print(f"💾 Saved all papers to '{filename}'")

        return self.all_papers
