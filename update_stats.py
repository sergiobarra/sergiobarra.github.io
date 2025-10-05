#!/usr/bin/env python3
"""
Simple script to update publication statistics in the publications page.
Run this script to update the statistics with current numbers from Google Scholar.
"""

import re
import os
from datetime import datetime

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

def main():
    """Main function with current statistics."""
    print("📊 Publication Statistics Updater")
    print("=" * 40)
    print()
    print("Current statistics from your Google Scholar profile:")
    print("• Publications: 52")
    print("• Citations: 967")
    print("• h-index: 18")
    print()
    
    # Update with current numbers
    update_publication_stats(
        publications=52,
        citations=967, 
        h_index=18
    )
    
    print()
    print("💡 To update in the future:")
    print("   1. Check your Google Scholar profile")
    print("   2. Update the numbers in this script")
    print("   3. Run: python update_stats.py")

if __name__ == "__main__":
    main()
