# Sergio Barrachina-Muñoz - Personal Academic Website

Welcome to my personal academic website showcasing my research in wireless networking, machine learning, and 5G/6G technologies.

🌐 **Live Website**: [https://sergiobarra.github.io](https://sergiobarra.github.io)

## 👨‍🔬 About Me

I am a **Senior Researcher and Technical Lead at CTTC (Centre Tecnològic de Telecomunicacions de Catalunya)** in Barcelona, Spain, specializing in the design, deployment, and management of next-generation telecom infrastructures powered by AI. I combine strong research experience (Ph.D., 50+ publications) with hands-on expertise in cloud-native systems, 5G/6G networks, and datacenter automation.

**Key Expertise:**
- AI-Powered Telecom Infrastructure & Next-Generation Networks
- Cloud-Native Systems & Datacenter Automation
- 5G/6G Network Design & Deployment
- MLOps & DevOps for Intelligent Systems
- Multi-Agent Frameworks for Autonomous Management
- Large-Scale Testbed Development & Project Leadership

## 📚 Research Highlights

- **52+ Publications** in top-tier venues (IEEE, Elsevier, ACM)
- **967+ Citations** with an **h-index of 18**
- **PhD in Information and Communication Technologies** (2021)
- **LAB leader** in 10+ European projects

## 🔗 Key Profiles

- **Google Scholar**: [View Publications](https://scholar.google.es/citations?user=bsDDtYYAAAAJ&hl=es&oi=sra)
- **ResearchGate**: [Professional Network](https://www.researchgate.net/profile/Sergio_Barrachina-Munoz)
- **LinkedIn**: [Connect with me](https://www.linkedin.com/in/sergiobarrachina/)
- **GitHub**: [Code & Projects](https://github.com/sergiobarra)

## 🛠️ Website Features

This website is built with **Jekyll** and deployed on **GitHub Pages**, featuring:

- **📖 Publications**: Live integration with Google Scholar profile
- **🎤 Talks**: Conference presentations and invited talks
- **📚 Teaching**: Course materials and academic activities
- **💼 Projects**: Research projects and collaborations
- **📄 CV**: Downloadable academic curriculum vitae

## 🚀 Local Development

To run this website locally:

```bash
# Clone the repository
git clone https://github.com/sergiobarra/sergiobarra.github.io.git
cd sergiobarra.github.io

# Install dependencies
bundle install

# Serve locally
bundle exec jekyll serve
```

The website will be available at `https://sergiobarra.github.io/`

## 📊 Automated Publication Management

This website includes automated tools for managing publications:

- **`update_publications.py`**: Fetch publications from Google Scholar
- **`update_stats.py`**: Update publication statistics
- **`scholar_fetcher.py`**: Advanced Google Scholar integration

```bash
# Update publication statistics
python update_stats.py

# Fetch new publications (requires CSV export from Google Scholar)
python update_publications.py
```

## 🏗️ Website Structure

```
├── _pages/           # Main website pages
├── _publications/    # Publication markdown files
├── _talks/          # Conference talks and presentations
├── _teaching/       # Teaching materials
├── _projects/       # Research projects
├── _data/           # Website configuration
├── images/          # Photos and graphics
└── assets/          # CSS, JS, and other assets
```

## 📝 Content Management

### Adding New Publications
1. Export your publications from Google Scholar as CSV
2. Run `python update_publications.py` to generate markdown files
3. Or manually create files in `_publications/` following the existing format

### Updating Statistics
```bash
# Edit update_stats.py with current numbers
python update_stats.py
```

### Adding New Talks
Create new markdown files in `_talks/` with the following front matter:
```yaml
---
title: "Your Talk Title"
venue: "Conference Name"
date: "2024-01-01"
location: "City, Country"
---
```

## 🔧 Technical Details

- **Framework**: Jekyll (Static Site Generator)
- **Theme**: AcademicPages (fork of Minimal Mistakes)
- **Hosting**: GitHub Pages
- **Deployment**: Automatic via GitHub Actions
- **Analytics**: Google Analytics integration

## 📄 License

This website template is based on [AcademicPages](https://github.com/academicpages/academicpages.github.io) and [Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/), both released under the MIT License.

## 📧 Contact

- **Email**: barrachina.sergio@gmail.com

---

*Last updated: October 2025*
