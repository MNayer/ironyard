#set page(width: 180pt, height: 120pt)

== New Publication

#line(length: 15%)

#text(size:9pt)[
_{{ author }}_
]

#text(size:10pt)[
{{ title }}
]


{% if multiple_publications %}
#align(bottom+center, text(size: 8pt)[
  {{ current_publication }} / {{ total_publications }}
])
{% endif %}
