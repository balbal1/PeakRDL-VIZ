{% filter indent(width=indent) %}
\viz_js
   box: {width: 90, height: {{height}}, strokeWidth: 1},
   init() {
      ret = {}
      ret.label = new fabric.Text("", {
            top: {{height}}/2-10,
            left: 45,
            originX: "center",
            originY: "center",
            fontFamily: "monospace",
            fontSize: 12
      })
      ret.value = new fabric.Text("", {
            top: {{height}}/2+10,
            left: 45,
            originX: "center",
            originY: "center",
            fontFamily: "monospace",
            fontSize: 12
      })
      return ret
   },
   renderFill() {
      let obj = this.getObjects()
      obj.label.set({fill: "black", text: "{{name}}"})
      obj.value.set({fill: "black", text: "{{register_size}}''h" + "0"})
      return `#F5A7A6`
   },
   where: {left: 450, top: {{top}}}
{% endfilter %}