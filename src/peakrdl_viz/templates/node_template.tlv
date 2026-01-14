{% filter indent(width=indent) %}
\viz_js
   box: {strokeWidth: 0},
   init() {
      return '/top_viz'.lib.init_node({
         width: {{node.width}},
         height: {{node.height}},
         fill: "#{{node.color}}",
      }, {
         top: {{node.height/2}},
         left: {{node.width/2}},
         fontSize: {{node.font_size}},
      })
   },
   render() {
      let obj = this.getObjects()
      obj.label.set({fill: "black", text: "{{node.name}}"})
   },
   where: {left: {{node.spacing}}, top: {{node.top}}}
{% endfilter %}