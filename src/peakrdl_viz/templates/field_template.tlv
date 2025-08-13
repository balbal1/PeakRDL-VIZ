{% filter indent(width=indent) %}{%- if implements_storage %}
$field_value[{{field_size-1}}:0] = {{module_name}}.field_storage.{{path}}.value;
$load_next = {{module_name}}.field_combo.{{path}}.load_next;{%- else %}
$field_value[{{field_size-1}}:0] = 0;
$load_next = 0;{%- endif %}
\viz_js
   box: {width: {{width}}, height: {{height}}, strokeWidth: 1},
   init() {
      return '/top_viz'.init_field({
         top: {{label_font_size}},
         left: {{width/2}},
         fontSize: {{label_font_size}},
      }, {
         top: {{height/2}},
         left: {{width/2}},
         fontSize: {{value_font_size}},
      }, {
         top: {{height - label_font_size}},
         left: {{width/2}},
         fontSize: {{label_font_size}},
      })
   },
   renderFill() {
      let obj = this.getObjects()
      let sw_write = this.sigVal(`{{module_name}}.cpuif_req`).step(-1).asInt() & this.sigVal(`{{module_name}}.decoded_req_is_wr`).step(-1).asInt()
      return '/top_viz'.render_field(obj, "{{radix}}" + '$field_value'.as{{radix_long}}Str(), "{{name}}", '$load_next'.step(-1).asBool(), sw_write)
   },
   where: {left: {{left}}, top: {{top}}}
{% endfilter %}