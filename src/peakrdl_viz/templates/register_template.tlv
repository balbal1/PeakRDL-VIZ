{% filter indent(width=indent) %}{%- if sv_flag %}
$register_value[{{node.size_bits-1}}:0] = {{node.fields_values}};
{% for word in node.words_array %}{%- if node.load_nexts[word] %}$register_load_next{{word}} = {{node.load_nexts[word]}};{%- endif %}
{% endfor %}{%- endif %}
\viz_js
   box: {strokeWidth: 0},
   init() {
      return '/top_viz'.lib.init_register([{% for word in node.words_array %}{
         width: {{node.word_width}},
         height: {{node.word_height}},
         left: {{node.width + node.spacing}},
         top: {{word * node.word_height - 2 * node.border_width}},
         strokeWidth: {{node.border_width}},
      },{% endfor %}], {
         width: {{node.width}},
         height: {{node.height}},
      }, {
         top: {{node.height/2-node.font_size}},
         left: {{node.width/2}},
         fontSize: {{node.font_size}},
      }, {
         top: {{node.height/2+node.font_size}},
         left: {{node.width/2}},
         fontSize: {{node.font_size}},
      })
   },
   render() {
      let obj = this.getObjects()
      let action_signals = []
      action_signals.push(this.sigVal(`{{module_name}}.cpuif_req`).step(-1))
      action_signals.push(this.sigVal(`{{module_name}}.decoded_req_is_wr`).step(-1))
      let fields = {{node.fields_slot}}
      let load_nexts = []{%- if sv_flag %}
      {% for word in node.words_array %}load_nexts.push('$register_load_next{{word}}')
      {% endfor %}return '/top_viz'.lib.render_register(obj, "{{node.name}}", {{node.size_bits}}, '$register_value'.asHexStr(), {{node.words_array[-1]+1}}, load_nexts, fields, action_signals){%- else %}
      {% for word in node.words_array %}if (this.sigVal(`{{module_name}}.decoded_req_is_wr`)) {
         load_nexts.push(this.sigVal(`{{module_name}}.decoded_req_is_wr`))
      }
      {% endfor %}return '/top_viz'.lib.render_register(obj, "{{node.name}}", {{node.size_bits}}, "0", {{node.words_array[-1]+1}}, load_nexts, fields, action_signals){%- endif %}
   },
   where: {left: {{node.left}}, top: {{node.top}}}
{% endfilter %}