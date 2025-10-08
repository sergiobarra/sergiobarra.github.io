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
from datetime import datetime

try:
    # scholarly is optional; used for automatic fetching
    from scholarly import scholarly  # type: ignore
    SCHOLARLY_AVAILABLE = True
except Exception:
    SCHOLARLY_AVAILABLE = False


def fetch_scholar_stats(scholar_id: str):
    """Fetch publications, citations, and h-index using scholarly.

    Returns a tuple (publications_count, total_citations, h_index), or None on failure.
    """
    if not SCHOLARLY_AVAILABLE:
        return None

    try:
        search_query = scholarly.search_author_id(scholar_id)
        author = scholarly.fill(search_query)

        publications_count = len(author.get('publications', []) or [])
        total_citations = int(author.get('citedby', 0) or 0)
        h_index = int(author.get('hindex', 0) or 0)

        return publications_count, total_citations, h_index
    except Exception:
        return None

def update_publication_stats(publications_file="_pages/publications.md", 
                           publications=52, citations=967, h_index=18):
    """Update publication statistics in the publications page."""
    
    try:
        # Read the current file
        with open(publications_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update statistics
        content = re.sub(
            r'<div style="font-size: 24px; font-weight: bold; color: #4285f4;">\d+</div>',
            f'<div style="font-size: 24px; font-weight: bold; color: #4285f4;">{publications}</div>',
            content
        )
        
        content = re.sub(
            r'<div style="font-size: 24px; font-weight: bold; color: #34a853;">\d+</div>',
            f'<div style="font-size: 24px; font-weight: bold; color: #34a853;">{citations}</div>',
            content
        )
        
        content = re.sub(
            r'<div style="font-size: 24px; font-weight: bold; color: #ea4335;">\d+</div>',
            f'<div style="font-size: 24px; font-weight: bold; color: #ea4335;">{h_index}</div>',
            content
        )
        
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

def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Update publication statistics on the publications page.")
    parser.add_argument("--publications-file", default="_pages/publications.md", help="Path to publications page file")
    parser.add_argument("--scholar-id", default="bsDDtYYAAAAJ", help="Google Scholar user ID")
    parser.add_argument("--publications", type=int, default=None, help="Manual override: publications count")
    parser.add_argument("--citations", type=int, default=None, help="Manual override: total citations")
    parser.add_argument("--h-index", type=int, default=None, help="Manual override: h-index")
    parser.add_argument("--no-fetch", action="store_true", help="Disable scholarly fetching and use provided/manual values")
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
        if SCHOLARLY_AVAILABLE:
            print("Attempting to fetch stats from Google Scholar…")
            fetched = fetch_scholar_stats(args.scholar_id)
            if fetched is None:
                print("Warning: Could not fetch stats automatically. Falling back to provided/manual values.")
        else:
            print("Note: scholarly is not installed. Install with: pip install scholarly")

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
        h_index=h_index
    )

    print()
    print("Tips:")
    print("- To fetch automatically, install scholarly: pip install scholarly")
    print(f"- Your Scholar profile: https://scholar.google.com/citations?user={args.scholar_id}")

if __name__ == "__main__":
    main()
