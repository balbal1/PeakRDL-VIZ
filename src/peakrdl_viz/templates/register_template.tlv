{% filter indent(width=indent) %}
$register_value[{{register_size-1}}:0] = {{concat_fields}};
{% for word in words %}{%- if concat_load_next[word] %}$register_load_next{{word}} = {{concat_load_next[word]}};{%- endif %}
{% endfor %}
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
      let load_nexts = []
      let fields = {{fields_slot}}
      {% for word in words %}load_nexts.push('$register_load_next{{word}}')
      {% endfor %}let action_signals = []
      action_signals.push(this.sigVal(`{{module_name}}.cpuif_req`).step(-1))
      action_signals.push(this.sigVal(`{{module_name}}.decoded_req_is_wr`).step(-1))
      return '/top_viz'.render_register(obj, "{{name}}", {{register_size}}, '$register_value'.asHexStr(), {{words[-1]+1}}, load_nexts, fields, action_signals)
   },
   where: {left: {{left}}, top: {{top}}}
{% endfilter %}