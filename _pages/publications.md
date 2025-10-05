---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

## 📚 **My Publications**

<div style="margin: 20px 0; border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #f9f9f9;">
  <h3 style="margin-top: 0; color: #333;">📚 Live Publications from Google Scholar</h3>
  
  <!-- Google Scholar Embed -->
  <iframe src="https://scholar.google.com/citations?user=bsDDtYYAAAAJ&hl=es&oi=sra&view_op=list_works&sortby=pubdate" 
          width="100%" 
          height="700" 
          frameborder="0" 
          scrolling="yes"
          style="border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
    <p>Your browser does not support iframes. Please visit <a href="{{author.googlescholar}}" target="_blank">my Google Scholar profile</a> directly.</p>
  </iframe>
  
  <div style="margin-top: 15px; text-align: center;">
    <a href="{{author.googlescholar}}" target="_blank" style="color: #4285f4; text-decoration: none;">
      🔗 Open in Google Scholar →
    </a>
  </div>
</div>

---

## 📊 **Publication Statistics**

<div style="display: flex; justify-content: space-around; margin: 20px 0; padding: 20px; background-color: #f8f9fa; border-radius: 8px; text-align: center;">
  <div>
    <div style="font-size: 24px; font-weight: bold; color: #4285f4;">52+</div>
    <div style="color: #666;">Publications</div>
  </div>
  <div>
    <div style="font-size: 24px; font-weight: bold; color: #34a853;">1000+</div>
    <div style="color: #666;">Citations</div>
  </div>
  <div>
    <div style="font-size: 24px; font-weight: bold; color: #ea4335;">15+</div>
    <div style="color: #666;">h-index</div>
  </div>
</div>

---

## 🎯 **Alternative Viewing Options**

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0;">
  <div style="padding: 15px; border: 1px solid #e0e0e0; border-radius: 8px; text-align: center;">
    <h4>📖 Google Scholar</h4>
    <p>Complete profile with citations and metrics</p>
    <a href="{{author.googlescholar}}" target="_blank" style="color: #4285f4;">View Profile</a>
  </div>
  
  <div style="padding: 15px; border: 1px solid #e0e0e0; border-radius: 8px; text-align: center;">
    <h4>🔬 ResearchGate</h4>
    <p>Professional network and collaboration</p>
    <a href="{{author.researchgate}}" target="_blank" style="color: #00cc88;">View Profile</a>
  </div>
  
  <div style="padding: 15px; border: 1px solid #e0e0e0; border-radius: 8px; text-align: center;">
    <h4>📄 Local Archive</h4>
    <p>Detailed publication records below</p>
    <a href="#local-publications" style="color: #ea4335;">View Archive</a>
  </div>
</div>

---

## 📄 **Complete Publication Archive** {#local-publications}

{% include base_path %}

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}
