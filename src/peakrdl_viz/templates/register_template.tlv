{% filter indent(width=indent) %}
$register_value[{{register_size-1}}:0] = {{concat_fields}};
\viz_js
   box: {strokeWidth: 0},
   init() {
      return '/top_viz'.init_register([{% for word in words %}{
         width: {{register_width}},
         height: {{register_height}},
         left: {{register_node_width + spacing}},
         top: {{word * register_height - 2 * border_width}},
         strokeWidth: {{border_width}},
      },{% endfor %}], {
         width: {{register_node_width}},
         height: {{height}},
      }, {
         top: {{height/2-register_font_size}},
         left: {{register_node_width/2}},
         fontSize: {{register_font_size}},
      }, {
         top: {{height/2+register_font_size}},
         left: {{register_node_width/2}},
         fontSize: {{register_font_size}},
      })
   },
   render() {
      let obj = this.getObjects()
      obj.label.set({fill: "black", text: "{{name}}"})
      obj.value.set({fill: "black", text: "{{register_size}}''h" + '$register_value'.asHexStr()})
   },
   where: {left: {{left}}, top: {{top}}}
{% endfilter %}