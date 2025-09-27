#set page(width: 74.51mm, height: 49.67mm)

== New Publication

#line(length: 15%)

#text(font: "Lato", size:10pt)[
_{{ author }}_
]

#text(size:12pt)[
{{ title }}
]


{% if multiple_publications %}
#align(bottom+center, text(size: 8pt)[
  {{ current_publication }} / {{ total_publications }}
])
{% endif %}
