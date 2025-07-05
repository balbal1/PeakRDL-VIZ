{% filter indent(width=indent) %}
$register_value[{{register_size-1}}:0] = {{concat_fields}};
\viz_js
   box: {strokeWidth: 0},
   init() {
      return '/top_viz'.init_register({{height}}, {{no_of_words}}, {{access_width}})
   },
   render() {
      let obj = this.getObjects()
      obj.label.set({fill: "black", text: "{{name}}"})
      obj.value.set({fill: "black", text: "{{register_size}}''h" + '$register_value'.asHexStr()})
   },
   where: {left: 0, top: {{top}}}
{% endfilter %}