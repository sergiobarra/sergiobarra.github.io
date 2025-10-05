# Updating Publications from Google Scholar

This guide explains how to update your website's publication list with your latest publications from Google Scholar.

## Method 1: Manual CSV Export (Recommended)

### Step 1: Export from Google Scholar
1. Go to your Google Scholar profile: https://scholar.google.es/citations?user=bsDDtYYAAAAJ&hl=es
2. Click on "Export" button (usually located near the top of your profile)
3. Select "CSV" format
4. Save the file as `publications.csv` in the root directory of your website

### Step 2: Run the Update Script
```bash
python update_publications.py
```

The script will:
- Read the CSV file
- Create new markdown files in `_publications/` directory
- Follow the same format as your existing publication files

## Method 2: Using Scholarly Library (Advanced)

### Installation
```bash
pip install -r publication_requirements.txt
```

### Usage
The `update_publications.py` script can be modified to use the scholarly library for automated fetching. However, note that Google Scholar has anti-scraping measures, so this approach may require additional setup.

## Method 3: Manual Addition

For individual publications, you can manually create files in the `_publications/` directory following this format:

```markdown
---
title: "Your Paper Title"
collection: publications
permalink: /publication/your-paper-slug
excerpt:
date: 2024-01-01
venue: 'Conference/Journal Name'
paperurl: 'https://link-to-paper.com'
citation: 'Author1, A., Author2, B., & Author3, C. (2024). Your Paper Title. <i>Conference/Journal Name</i>.'

---
**Abstract:** Your paper abstract here.

[Download paper here](https://link-to-paper.com)
```

## File Naming Convention

Publication files should follow this naming pattern:
`{firstauthor}{year}{short-title}.md`

Examples:
- `barrachina2024neural.md`
- `barrachina2023wireless.md`

## Current Publications

Your website currently has these publication files:
- adame2018hare.md
- barrachina2015goat.md
- barrachina2017learning.md
- barrachina2017multihop.md
- barrachina2019dynamic.md
- barrachina2019komondor.md
- barrachina2019online.md
- barrachina2019tooverlap.md
- barrachina2019towards.md
- barrachina2020wifi.md
- barrachina2021multi.md
- barrachina2021stateless.md
- barrachina2021wificb.md
- lopez2019sdn.md
- wilhelmi2017collaborative.md
- wilhelmi2018potential.md
- wilhelmi2019ontheperformance.md
- wilhelmi2020aflexible.md
- wilhelmi2020spatialreuse.md
- wilhelmi2022end.md

## Troubleshooting

### CSV Import Issues
- Ensure the CSV file has the correct column headers
- Check that the file is saved as UTF-8 encoding
- Verify that the file is in the root directory

### File Creation Issues
- Check that the `_publications/` directory exists
- Ensure you have write permissions
- Verify that the Python script can access the directory

### Google Scholar Access
- If automated fetching doesn't work, use the manual CSV export method
- Google Scholar may block automated requests - this is normal
- Consider using the scholarly library with proper rate limiting

## Next Steps

1. Export your publications from Google Scholar as CSV
2. Run the update script
3. Check the generated files in `_publications/`
4. Test your website locally to ensure everything displays correctly
5. Commit and push changes to GitHub

## Support

If you encounter issues:
1. Check the error messages in the console
2. Verify your Google Scholar profile is public
3. Ensure all required files are present
4. Check the file permissions and directory structure
