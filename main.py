from ResearchClass import ResearchOrchestrator
orchestrator = ResearchOrchestrator(topic="Machine Learning", max_papers=10)
orchestrator.run_pipeline(search_query="Natural Language Processing", top_k=5, clear_before_push=True)
