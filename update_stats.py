#!/usr/bin/env python3
"""
Update publication statistics on the publications page.

Features:
- Attempts to fetch live stats from Google Scholar via `scholarly` when available
- Falls back to provided/manual values if fetching is unavailable or fails
- CLI arguments to set scholar id, override values, and target file
"""

import re
import os
import sys
import argparse
import json
import time
import concurrent.futures
from datetime import datetime

try:
    # scholarly is optional; used for automatic fetching
    from scholarly import scholarly  # type: ignore
    SCHOLARLY_AVAILABLE = True
except Exception:
    SCHOLARLY_AVAILABLE = False

try:
    # requests is optional; used for SerpAPI fallback
    import requests  # type: ignore
    REQUESTS_AVAILABLE = True
except Exception:
    REQUESTS_AVAILABLE = False


def fetch_scholar_stats(scholar_id: str):
    """Fetch publications, citations, and h-index using scholarly.

    Returns a tuple (publications_count, total_citations, h_index), or None on failure.
    """
    if not SCHOLARLY_AVAILABLE:
        return None

    try:
        print(f"[fetch] Starting scholar fetch for ID={scholar_id}")
        search_query = scholarly.search_author_id(scholar_id)
        author = scholarly.fill(search_query)

        publications_count = len(author.get('publications', []) or [])
        total_citations = int(author.get('citedby', 0) or 0)
        h_index = int(author.get('hindex', 0) or 0)

        print(f"[fetch] Success: pubs={publications_count}, citations={total_citations}, h={h_index}")
        return publications_count, total_citations, h_index
    except Exception:
        print("[fetch] Error during scholar fetch; will fallback if possible")
        return None


def fetch_scholar_stats_with_timeout(scholar_id: str, timeout_seconds: int = 45):
    """Run fetch_scholar_stats with a hard timeout to avoid hanging in CI."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(fetch_scholar_stats, scholar_id)
        try:
            return future.result(timeout=timeout_seconds)
        except concurrent.futures.TimeoutError:
            print(f"[fetch] Timeout after {timeout_seconds}s; using fallback values")
            return None


def fetch_scholar_stats_serpapi(scholar_id: str, api_key: str):
    """Fetch publications, citations, and h-index using SerpAPI.
    
    Returns a tuple (publications_count, total_citations, h_index), or None on failure.
    """
    if not REQUESTS_AVAILABLE:
        print("[serpapi] requests library not available")
        return None
    
    try:
        print(f"[serpapi] Starting SerpAPI fetch for ID={scholar_id}")

        # SerpAPI Google Scholar Author endpoint: use author_id (not profiles search)
        url = "https://serpapi.com/search.json"
        params = {
            "engine": "google_scholar_author",
            "author_id": scholar_id,
            "api_key": api_key,
            "hl": "en"
        }

        response = requests.get(url, params=params, timeout=20)
        if response.status_code != 200:
            try:
                payload = response.json()
                error_msg = payload.get("error") or payload.get("message") or "HTTP error"
            except Exception:
                error_msg = "HTTP error"
            print(f"[serpapi] HTTP {response.status_code}: {error_msg}")
            return None

        data = response.json()

        # Extract stats per SerpAPI docs
        # Publications: prefer author.articles_count (total publications)
        author_obj = data.get("author", {}) or {}
        publications_count = int(author_obj.get("articles_count", 0) or 0)
        if not publications_count:
            # Fallback: count all articles via pagination
            articles = data.get("articles", []) or []
            publications_count = len(articles)
            try:
                pagination = data.get("serpapi_pagination", {}) or {}
                next_url = pagination.get("next")
                pages_fetched = 0
                while next_url and pages_fetched < 10:  # safety cap
                    # Ensure api_key is present (avoid leaking in logs)
                    if "api_key=" not in next_url:
                        sep = '&' if '?' in next_url else '?'
                        next_url = f"{next_url}{sep}api_key=REDACTED"
                        # Use real key in request, not in logged URL
                        req_url = next_url.replace("api_key=REDACTED", f"api_key={api_key}")
                    else:
                        req_url = next_url
                    page_resp = requests.get(req_url, timeout=20)
                    if page_resp.status_code != 200:
                        break
                    page_data = page_resp.json()
                    publications_count += len(page_data.get("articles", []) or [])
                    pagination = page_data.get("serpapi_pagination", {}) or {}
                    next_url = pagination.get("next")
                    pages_fetched += 1
            except Exception:
                # If pagination fails, keep current count
                pass

        # Citations and h-index from cited_by.table rows
        cited_by = data.get("cited_by", {}) or {}
        table = cited_by.get("table", []) or []
        total_citations = 0
        h_index = 0
        if isinstance(table, list):
            if len(table) > 0 and isinstance(table[0], dict):
                total_citations = int((((table[0].get("citations", {}) or {}).get("all", 0)) or 0))
            if len(table) > 1 and isinstance(table[1], dict):
                h_index = int((((table[1].get("h_index", {}) or {}).get("all", 0)) or 0))
        if not total_citations:
            total_citations = int(((cited_by.get("citations", {}) or {}).get("all", 0)) or 0)
        if not h_index:
            h_index = int(((cited_by.get("h_index", {}) or {}).get("all", 0)) or 0)

        print(f"[serpapi] Success: pubs={publications_count}, citations={total_citations}, h={h_index}")
        return publications_count, total_citations, h_index

    except requests.RequestException as e:
        # Avoid printing full URL with key
        print(f"[serpapi] Request error: {str(e)}")
        return None
    except Exception as e:
        print(f"[serpapi] Error during SerpAPI fetch: {e}")
        return None


def fetch_scholar_stats_with_fallback(scholar_id: str, serpapi_key: str = None, timeout_seconds: int = 45):
    """Try scholarly first, then SerpAPI as fallback (to save SerpAPI credits)."""

    # Try scholarly first
    if SCHOLARLY_AVAILABLE:
        print("Attempting to fetch stats from Google Scholar via scholarly…")
        result = fetch_scholar_stats_with_timeout(scholar_id, timeout_seconds)
        if result is not None:
            return result
        print("scholarly failed, trying SerpAPI fallback…")

    # Try SerpAPI fallback
    if serpapi_key and REQUESTS_AVAILABLE:
        print("Attempting to fetch stats from Google Scholar via SerpAPI…")
        result = fetch_scholar_stats_serpapi(scholar_id, serpapi_key)
        if result is not None:
            return result
        print("SerpAPI also failed")

    return None

def update_publication_stats(publications_file="_pages/publications.md", 
                           publications=52, citations=967, h_index=18, verbose=False):
    """Update publication statistics in the publications page."""
    
    try:
        # Read the current file
        if verbose:
            print(f"[update] Opening file: {publications_file}")
        with open(publications_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update statistics
        content, repl_count_pubs = re.subn(
            r'<div style="font-size: 24px; font-weight: bold; color: #4285f4;">\d+</div>',
            f'<div style="font-size: 24px; font-weight: bold; color: #4285f4;">{publications}</div>',
            content
        )
        
        content, repl_count_cit = re.subn(
            r'<div style="font-size: 24px; font-weight: bold; color: #34a853;">\d+</div>',
            f'<div style="font-size: 24px; font-weight: bold; color: #34a853;">{citations}</div>',
            content
        )
        
        content, repl_count_h = re.subn(
            r'<div style="font-size: 24px; font-weight: bold; color: #ea4335;">\d+</div>',
            f'<div style="font-size: 24px; font-weight: bold; color: #ea4335;">{h_index}</div>',
            content
        )
        if verbose:
            print(f"[update] Replacements -> pubs:{repl_count_pubs} cit:{repl_count_cit} h:{repl_count_h}")
        
        # Write the updated content
        with open(publications_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Statistics updated successfully!")
        print(f"   Publications: {publications}")
        print(f"   Citations: {citations}")
        print(f"   h-index: {h_index}")
        print(f"   Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Error updating statistics: {e}")

def update_about_h_index(about_file="_pages/about.md", h_index=18, verbose=False):
    """Update h-index value in the about page."""
    
    try:
        # Read the current file
        if verbose:
            print(f"[update] Opening file: {about_file}")
        with open(about_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update h-index in the text pattern: (h-index \d+)
        content, repl_count = re.subn(
            r'\(h-index \d+\)',
            f'(h-index {h_index})',
            content
        )
        
        if verbose:
            print(f"[update] Replacements -> h-index:{repl_count}")
        
        # Write the updated content
        with open(about_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        if repl_count > 0:
            print(f"✅ h-index updated in about page: {h_index}")
        else:
            print(f"⚠️  No h-index pattern found in about page (expected pattern: 'h-index XX')")
        
    except Exception as e:
        print(f"❌ Error updating h-index in about page: {e}")

def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Update publication statistics on the publications page.")
    parser.add_argument("--publications-file", default="_pages/publications.md", help="Path to publications page file")
    parser.add_argument("--about-file", default="_pages/about.md", help="Path to about page file")
    parser.add_argument("--scholar-id", default="bsDDtYYAAAAJ", help="Google Scholar user ID")
    parser.add_argument("--publications", type=int, default=None, help="Manual override: publications count")
    parser.add_argument("--citations", type=int, default=None, help="Manual override: total citations")
    parser.add_argument("--h-index", type=int, default=None, help="Manual override: h-index")
    parser.add_argument("--no-fetch", action="store_true", help="Disable scholarly fetching and use provided/manual values")
    parser.add_argument("--serpapi-key", default=None, help="SerpAPI key for fallback fetching (or set SERPAPI_KEY env var)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose debug logs")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    print("📊 Publication Statistics Updater")
    print("=" * 40)
    print()

    publications = args.publications
    citations = args.citations
    h_index = args.h_index

    fetched = None
    if not args.no_fetch:
        # Get SerpAPI key from args or environment
        serpapi_key = args.serpapi_key or os.getenv('SERPAPI_KEY')
        
        fetched = fetch_scholar_stats_with_fallback(args.scholar_id, serpapi_key, timeout_seconds=45)
        if fetched is None:
            print("Warning: Could not fetch stats automatically. Falling back to provided/manual values.")
            if not SCHOLARLY_AVAILABLE:
                print("Note: scholarly is not installed. Install with: pip install scholarly")
            if not REQUESTS_AVAILABLE:
                print("Note: requests is not installed. Install with: pip install requests")
            if not serpapi_key:
                print("Note: SerpAPI key not provided. Set --serpapi-key or SERPAPI_KEY env var")

    if fetched is not None:
        publications, citations, h_index = fetched

    # Provide sane defaults if nothing supplied or fetched
    if publications is None:
        publications = 52
    if citations is None:
        citations = 967
    if h_index is None:
        h_index = 18

    print("Using statistics:")
    print(f"• Publications: {publications}")
    print(f"• Citations: {citations}")
    print(f"• h-index: {h_index}")
    print()

    update_publication_stats(
        publications_file=args.publications_file,
        publications=publications,
        citations=citations,
        h_index=h_index,
        verbose=args.verbose
    )

    update_about_h_index(
        about_file=args.about_file,
        h_index=h_index,
        verbose=args.verbose
    )

    print()
    print("Tips:")
    print("- To fetch automatically, install: pip install scholarly requests")
    print("- For SerpAPI fallback, set SERPAPI_KEY environment variable or use --serpapi-key")
    print(f"- Your Scholar profile: https://scholar.google.com/citations?user={args.scholar_id}")

if __name__ == "__main__":
    main()
