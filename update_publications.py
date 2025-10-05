#!/usr/bin/env python3
"""
Script to update Jekyll publication files from Google Scholar profile.
This script fetches publications from Google Scholar and creates/updates
the corresponding markdown files in the _publications directory.
"""

import requests
import json
import re
import os
from datetime import datetime
from urllib.parse import quote
import time

class GoogleScholarUpdater:
    def __init__(self, scholar_id, publications_dir="_publications"):
        self.scholar_id = scholar_id
        self.publications_dir = publications_dir
        self.base_url = "https://scholar.google.es/citations"
        
    def fetch_publications(self):
        """
        Fetch publications from Google Scholar profile.
        Note: This is a simplified approach. In practice, you might need to use
        a library like scholarly or implement proper scraping with rate limiting.
        """
        try:
            # This is a placeholder - in practice, you'd need to implement
            # proper web scraping or use an API
            print(f"Fetching publications for scholar ID: {self.scholar_id}")
            print("Note: Direct Google Scholar scraping requires additional setup.")
            print("Please see the instructions below for manual export.")
            
            # For now, return empty list - user will need to manually provide data
            return []
            
        except Exception as e:
            print(f"Error fetching publications: {e}")
            return []
    
    def create_publication_file(self, publication_data):
        """Create a Jekyll publication markdown file."""
        # Generate filename from title
        title_slug = re.sub(r'[^\w\s-]', '', publication_data.get('title', 'untitled'))
        title_slug = re.sub(r'[-\s]+', '-', title_slug).lower()
        
        # Generate author slug for filename
        authors = publication_data.get('authors', '')
        author_slug = 'barrachina'
        year = publication_data.get('year', datetime.now().year)
        
        filename = f"{author_slug}{year}{title_slug[:20]}.md"
        filepath = os.path.join(self.publications_dir, filename)
        
        # Create front matter
        front_matter = f"""---
title: "{publication_data.get('title', 'Untitled')}"
collection: publications
permalink: /publication/{title_slug[:30]}
excerpt:
date: {publication_data.get('date', f'{year}-01-01')}
venue: '{publication_data.get('venue', 'Unknown Venue')}'
paperurl: '{publication_data.get('url', '')}'
citation: '{publication_data.get('citation', '')}'

---
"""
        
        # Add abstract if available
        content = front_matter
        if publication_data.get('abstract'):
            content += f"**Abstract:** {publication_data.get('abstract')}\n\n"
        
        # Add download link if available
        if publication_data.get('url'):
            content += f"[Download paper here]({publication_data.get('url')})\n"
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Created publication file: {filename}")
        return filepath
    
    def update_from_csv(self, csv_file):
        """Update publications from a CSV file exported from Google Scholar."""
        import csv
        
        publications = []
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Map CSV columns to our format
                    pub_data = {
                        'title': row.get('Title', ''),
                        'authors': row.get('Authors', ''),
                        'year': row.get('Year', ''),
                        'venue': row.get('Publication venue', ''),
                        'url': row.get('URL', ''),
                        'abstract': row.get('Abstract', ''),
                        'citation': self.format_citation(row)
                    }
                    publications.append(pub_data)
        
        except FileNotFoundError:
            print(f"CSV file {csv_file} not found.")
            return []
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return []
        
        return publications
    
    def format_citation(self, row):
        """Format citation from CSV row data."""
        authors = row.get('Authors', '')
        title = row.get('Title', '')
        venue = row.get('Publication venue', '')
        year = row.get('Year', '')
        
        # Simple citation format
        citation = f"{authors} ({year}). {title}. <i>{venue}</i>."
        return citation

def main():
    """Main function to update publications."""
    scholar_id = "bsDDtYYAAAAJ"
    updater = GoogleScholarUpdater(scholar_id)
    
    print("Google Scholar Publication Updater")
    print("=" * 40)
    print()
    print("To update your publications, you have several options:")
    print()
    print("1. MANUAL CSV EXPORT (Recommended):")
    print("   - Go to your Google Scholar profile:")
    print(f"   - https://scholar.google.es/citations?user={scholar_id}&hl=es")
    print("   - Click 'Export' → 'CSV'")
    print("   - Save the file as 'publications.csv' in this directory")
    print("   - Run: python update_publications.py --csv publications.csv")
    print()
    print("2. MANUAL PUBLICATION ADDITION:")
    print("   - Create publication files manually in the _publications/ directory")
    print("   - Follow the format of existing files")
    print()
    print("3. AUTOMATED APPROACH (Advanced):")
    print("   - Install scholarly library: pip install scholarly")
    print("   - Modify this script to use the scholarly library")
    print("   - Note: Google Scholar has anti-scraping measures")
    print()
    
    # Check if CSV file exists
    csv_file = "publications.csv"
    if os.path.exists(csv_file):
        print(f"Found {csv_file}, processing...")
        publications = updater.update_from_csv(csv_file)
        
        print(f"\nProcessing {len(publications)} publications...")
        for pub in publications:
            updater.create_publication_file(pub)
        
        print(f"\nSuccessfully updated {len(publications)} publications!")
    else:
        print(f"No {csv_file} found. Please export your publications from Google Scholar first.")

if __name__ == "__main__":
    main()
