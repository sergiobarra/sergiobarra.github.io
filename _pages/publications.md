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
  
  <div style="text-align: center; padding: 40px 20px; background-color: #fff; border-radius: 8px; border: 2px dashed #4285f4;">
    <div style="font-size: 48px; margin-bottom: 20px;">📖</div>
    <h4 style="color: #333; margin-bottom: 15px;">View My Complete Publication Profile</h4>
    <p style="color: #666; margin-bottom: 25px; line-height: 1.6;">
      For the best experience viewing my publications with live citations, metrics, and full abstracts, 
      please visit my Google Scholar profile directly.
    </p>
    <a href="https://scholar.google.es/citations?user=bsDDtYYAAAAJ&hl=es&oi=sra" target="_blank" 
       style="display: inline-block; background-color: #4285f4; color: white; padding: 12px 24px; 
              text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px;
              box-shadow: 0 2px 4px rgba(66, 133, 244, 0.3); transition: all 0.2s;">
      🔗 Open Google Scholar Profile
    </a>
    <p style="color: #888; font-size: 14px; margin-top: 15px;">
      Opens in a new tab • Always up-to-date • Full citation metrics
    </p>
  </div>
</div>

---

## 📊 **Publication Statistics**

<div style="display: flex; justify-content: space-around; margin: 20px 0; padding: 20px; background-color: #f8f9fa; border-radius: 8px; text-align: center;">
  <div>
    <div style="font-size: 24px; font-weight: bold; color: #4285f4;">51</div>
    <div style="color: #666;">Publications</div>
  </div>
  <div>
    <div style="font-size: 24px; font-weight: bold; color: #34a853;">1048</div>
    <div style="color: #666;">Citations</div>
  </div>
  <div>
    <div style="font-size: 24px; font-weight: bold; color: #ea4335;">19</div>
    <div style="color: #666;">h-index</div>
  </div>
</div>

---

## 🎯 **Alternative Viewing Options**

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0;">
  <div style="padding: 15px; border: 1px solid #e0e0e0; border-radius: 8px; text-align: center;">
    <h4>📖 Google Scholar</h4>
    <p>Complete profile with citations and metrics</p>
    <a href="https://scholar.google.es/citations?user=bsDDtYYAAAAJ&hl=es&oi=sra" target="_blank" style="color: #4285f4;">View Profile</a>
  </div>
  
  <div style="padding: 15px; border: 1px solid #e0e0e0; border-radius: 8px; text-align: center;">
    <h4>🔬 ResearchGate</h4>
    <p>Professional network and collaboration</p>
    <a href="https://www.researchgate.net/profile/Sergio_Barrachina-Munoz" target="_blank" style="color: #00cc88;">View Profile</a>
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
