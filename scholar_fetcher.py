#!/usr/bin/env python3
"""
Advanced Google Scholar publication fetcher using the scholarly library.
This script attempts to fetch publications directly from Google Scholar.
"""

import os
import re
import time
from datetime import datetime
from scholarly import scholarly

class ScholarFetcher:
    def __init__(self, scholar_id, publications_dir="_publications"):
        self.scholar_id = scholar_id
        self.publications_dir = publications_dir
        
    def fetch_author_profile(self):
        """Fetch the author's profile from Google Scholar."""
        try:
            print(f"Fetching profile for scholar ID: {self.scholar_id}")
            
            # Search for the author by ID
            search_query = scholarly.search_author_id(self.scholar_id)
            author = scholarly.fill(search_query)
            
            return author
        except Exception as e:
            print(f"Error fetching author profile: {e}")
            return None
    
    def get_publications(self, author):
        """Extract publications from author profile."""
        if not author:
            return []
        
        publications = []
        
        try:
            print(f"Found author: {author.get('name', 'Unknown')}")
            print(f"Total publications: {len(author.get('publications', []))}")
            
            for pub in author.get('publications', []):
                # Fill publication details
                try:
                    filled_pub = scholarly.fill(pub)
                    publications.append(filled_pub)
                    time.sleep(1)  # Rate limiting
                except Exception as e:
                    print(f"Error filling publication details: {e}")
                    # Add basic info if detailed fetch fails
                    publications.append(pub)
                    time.sleep(1)
                    
        except Exception as e:
            print(f"Error extracting publications: {e}")
        
        return publications
    
    def format_publication_data(self, pub):
        """Format publication data for Jekyll."""
        # Extract title
        title = pub.get('bib', {}).get('title', 'Untitled')
        
        # Extract authors
        authors = pub.get('bib', {}).get('author', 'Unknown Authors')
        
        # Extract year
        year = pub.get('bib', {}).get('pub_year', datetime.now().year)
        
        # Extract venue
        venue = pub.get('bib', {}).get('venue', 'Unknown Venue')
        
        # Extract URL
        url = pub.get('pub_url', '')
        
        # Extract abstract
        abstract = pub.get('bib', {}).get('abstract', '')
        
        # Format citation
        citation = f"{authors} ({year}). {title}. <i>{venue}</i>."
        
        return {
            'title': title,
            'authors': authors,
            'year': year,
            'venue': venue,
            'url': url,
            'abstract': abstract,
            'citation': citation,
            'date': f"{year}-01-01"
        }
    
    def create_publication_file(self, pub_data):
        """Create a Jekyll publication markdown file."""
        # Generate filename
        title_slug = re.sub(r'[^\w\s-]', '', pub_data.get('title', 'untitled'))
        title_slug = re.sub(r'[-\s]+', '-', title_slug).lower()
        
        # Use first author and year for filename
        authors = pub_data.get('authors', '')
        if 'Barrachina-Muñoz' in authors or 'Barrachina' in authors:
            author_slug = 'barrachina'
        else:
            # Extract first author's last name
            first_author = authors.split(',')[0].strip()
            author_slug = first_author.split()[-1].lower() if first_author else 'unknown'
        
        year = pub_data.get('year', datetime.now().year)
        filename = f"{author_slug}{year}{title_slug[:20]}.md"
        filepath = os.path.join(self.publications_dir, filename)
        
        # Check if file already exists
        if os.path.exists(filepath):
            print(f"File {filename} already exists, skipping...")
            return None
        
        # Create front matter
        front_matter = f"""---
title: "{pub_data.get('title', 'Untitled')}"
collection: publications
permalink: /publication/{title_slug[:30]}
excerpt:
date: {pub_data.get('date', f'{year}-01-01')}
venue: '{pub_data.get('venue', 'Unknown Venue')}'
paperurl: '{pub_data.get('url', '')}'
citation: '{pub_data.get('citation', '')}'

---
"""
        
        # Add content
        content = front_matter
        if pub_data.get('abstract'):
            content += f"**Abstract:** {pub_data.get('abstract')}\n\n"
        
        if pub_data.get('url'):
            content += f"[Download paper here]({pub_data.get('url')})\n"
        
        # Write file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Created publication file: {filename}")
            return filepath
        except Exception as e:
            print(f"Error creating file {filename}: {e}")
            return None
    
    def update_publications(self):
        """Main method to update publications."""
        print("Starting Google Scholar publication update...")
        
        # Fetch author profile
        author = self.fetch_author_profile()
        if not author:
            print("Failed to fetch author profile. Please check your internet connection and try again.")
            return
        
        # Get publications
        publications = self.get_publications(author)
        if not publications:
            print("No publications found.")
            return
        
        print(f"\nProcessing {len(publications)} publications...")
        
        # Create publication files
        created_files = []
        for pub in publications:
            pub_data = self.format_publication_data(pub)
            filepath = self.create_publication_file(pub_data)
            if filepath:
                created_files.append(filepath)
            time.sleep(0.5)  # Rate limiting
        
        print(f"\nSuccessfully created {len(created_files)} new publication files!")
        
        if created_files:
            print("\nCreated files:")
            for filepath in created_files:
                print(f"  - {os.path.basename(filepath)}")

def main():
    """Main function."""
    scholar_id = "bsDDtYYAAAAJ"
    fetcher = ScholarFetcher(scholar_id)
    
    print("Google Scholar Publication Fetcher")
    print("=" * 40)
    print()
    print("Note: This script uses the scholarly library to fetch publications.")
    print("Google Scholar may block requests if too many are made quickly.")
    print("The script includes rate limiting to avoid this.")
    print()
    
    try:
        fetcher.update_publications()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("Please try the manual CSV export method instead.")

if __name__ == "__main__":
    main()
