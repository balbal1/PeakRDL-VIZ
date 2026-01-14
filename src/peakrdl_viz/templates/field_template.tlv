{% filter indent(width=indent) %}{%- if sv_flag %}{%- if node.value_exists %}
$field_value[{{node.width-1}}:0] = {{module_name}}.field_storage.{{node.path}}.value;
$load_next = {{module_name}}.field_combo.{{node.path}}.load_next;{%- else %}
$field_value[{{node.width-1}}:0] = 0;
$load_next = 0;{%- endif %}{%- endif %}
\viz_js
   box: {width: {{node.spaceview_width}}, height: {{node.spaceview_height}}, strokeWidth: 1},
   init() {
      return '/top_viz'.lib.init_field({
         top: {{node.label_font_size}},
         left: {{node.spaceview_width/2}},
         fontSize: {{node.label_font_size}},
      }, {
         top: {{node.spaceview_height/2}},
         left: {{node.spaceview_width/2}},
         fontSize: {{node.value_font_size}},
      }, {
         top: {{node.spaceview_height - node.label_font_size}},
         left: {{node.spaceview_width/2}},
         fontSize: {{node.label_font_size}},
      })
   },
   renderFill() {
      let obj = this.getObjects()
      let sw_read = this.sigVal(`{{module_name}}.cpuif_req`).step(-1).asInt() & !this.sigVal(`{{module_name}}.decoded_req_is_wr`).step(-1).asInt()
      let sw_write = this.sigVal(`{{module_name}}.cpuif_req`).step(-1).asInt() & this.sigVal(`{{module_name}}.decoded_req_is_wr`).step(-1).asInt(){%- if sv_flag %}
      return '/top_viz'.lib.render_field(obj, "{{node.radix}}" + '$field_value'.as{{node.radix_name}}Str(), "{{node.name}}", '$load_next'.step(-1).asBool(), sw_write){%- elif node.value_exists %}
      let field_value = this.sigVal(`{{module_name}}.field_storage.{{node.path}}.value`).as{{node.radix_name}}Str()
      let load_next = this.sigVal(`{{module_name}}.field_combo.{{node.path}}.load_next`).step(-1).asBool()
      return '/top_viz'.lib.render_field(obj, "{{node.radix}}" + field_value, "{{node.name}}", load_next, sw_write){%- endif %}
   },
   where: {left: {{node.left}}, top: {{node.top}}}
{% endfilter %}