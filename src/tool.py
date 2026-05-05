import requests
import os
from typing import List

LINKUP_KEY = os.getenv("LINKUP_API_KEY")

def scrape_devops_fix(query: str) -> str:
    """FREE Linkup API: Latest Docker/K8s solutions"""
    url = "https://api.linkup.so/v1/search"
    payload = {
        "query": f"{query} docker kubernetes fix solution 2026",
        "num_results": 3
    }
    headers = {"Authorization": f"Bearer {LINKUP_KEY}"}
    
    try:
        resp = requests.post(url, json=payload, headers=headers)
        results = resp.json().get("results", [])
        return "\n".join([r["content"][:500] for r in results])
    except:
        return "Fallback: docker-compose up --scale service=2"
