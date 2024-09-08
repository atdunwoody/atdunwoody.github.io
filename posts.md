---
layout: page
title: "Projects"
permalink: /projects/
main_nav: true
---

<h1>Projects</h1>

<ul class="projects-list">
{% for page in site.pages %}
  {% if page.categories contains "projects" %}
    <li>
      <strong>
        <a href="{{ page.url | prepend: site.baseurl }}">{{ page.title }}</a>
      </strong>
    </li>
  {% endif %}
{% endfor %}
</ul>
<br>
