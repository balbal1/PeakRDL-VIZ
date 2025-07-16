{% filter indent(width=indent) %}
\viz_js
   box: {strokeWidth: 0},
   init() {
      return '/top_viz'.init_node({
         width: {{node_width}},
         height: {{height}},
         fill: "#{{color}}",
      }, {
         top: {{height/2}},
         left: {{node_width/2}},
         fontSize: {{node_font_size}},
      })
   },
   render() {
      let obj = this.getObjects()
      obj.label.set({fill: "black", text: "{{name}}"})
   },
   where: {left: {{spacing}}, top: {{top}}}
{% endfilter %}