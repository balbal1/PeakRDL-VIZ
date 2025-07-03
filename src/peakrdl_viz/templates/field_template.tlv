{% filter indent(width=indent) %}
\viz_js
   box: {width: {{width}}, height: 70, strokeWidth: 1},
   init() {
      ret = {}
      ret.label = new fabric.Text("", {
            top: 10,
            left: {{width}}/2,
            originX: "center",
            originY: "center",
            fontFamily: "monospace",
            fontSize: {{label_font_size}}
      })
      ret.value = new fabric.Text("", {
            top: 35,
            left: {{width}}/2,
            originX: "center",
            originY: "center",
            fontFamily: "monospace",
            fontSize: {{value_font_size}}
      })
      ret.action = new fabric.Text("", {
            top: 60,
            left: {{width}}/2,
            originX: "center",
            originY: "center",
            fontFamily: "monospace",
            fontSize: {{label_font_size}}
      })
      return ret
   },
   renderFill() {
      let obj = this.getObjects()
      let field = this.sigVal(`{{module_name}}.field_storage.{{path}}.value`)
      if (field) {
         obj.value.set({text: "{{field_size}}''{{radix}}" + field.as{{radix_long}}Str()})
         obj.label.set({fill: "black", text: "{{name}}"})
         if (field.asInt() == field.step(-1).asInt()) {
            obj.value.set({fill: "black"})
            obj.action.set({fill: "black", text: ""})
            return `#F3F5A9`
         } else {
            obj.value.set({fill: "blue"})
            let sw_write = this.sigVal(`{{module_name}}.cpuif_req`).step(-1).asInt() & this.sigVal(`{{module_name}}.decoded_req_is_wr`).step(-1).asInt()
            if (sw_write) {
               obj.action.set({fill: "black", text: "sw write"})
            } else {
               obj.action.set({fill: "black", text: "hw write"})
            }
            return `#77DD77`
         }
      } else {
         obj.value.set({fill: "black", text: "error"})
         return `#F3F5A9`
      }
   },
   where: {left: {{left}} - 450, top: {{top}}-10}
{% endfilter %}