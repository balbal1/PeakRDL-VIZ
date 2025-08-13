\m5_TLV_version 1d: tl-x.org
{% raw %}{% endraw %}
{%- if package_content %}
\SV
{% raw %}{% endraw %}
{{ package_content }}
{%- endif %}{% raw %}
{% endraw %}
{%- if module_content %}
// ---
// Top
// ---
\SV
   m5_makerchip_module
   {{module_name}}_pkg::{{module_name}}__in_t hwif_in;
   {{module_name}}_pkg::{{module_name}}__out_t hwif_out;

\TLV
   
   $reset = *reset;
   $s_apb_pwrite = 1;

{{viz_code.get_hw_randomization_lines()}}

   {{ module_name }} {{ module_name }}(*clk, $reset, $s_apb_psel, $s_apb_penable, $s_apb_pwrite, $s_apb_paddr[{{viz_code.design_sizer.max_address}}:0], $s_apb_pwdata[{{access_width-1}}:0], $s_apb_pready, $s_apb_prdata[{{access_width-1}}:0], $s_apb_pslverr, *hwif_in, *hwif_out);

   *passed = *cyc_cnt > 100;
   *failed = 1'b0;
{% else %}
\TLV
{%- endif %}

   /top_viz
{{viz_code.get_timeline_lines()}}
      \viz_js
         box: {strokeWidth: 0},
         lib: {
            init_field: (label, value, action) => {
               let ret = {}
               ret.label = new fabric.Text("", {
                  ...label,
                  originX: "center",
                  originY: "center",
                  fontFamily: "monospace",
               })
               ret.value = new fabric.Text("", {
                  ...value,
                  originX: "center",
                  originY: "center",
                  fontFamily: "monospace",
               })
               ret.action = new fabric.Text("", {
                  ...action,
                  originX: "center",
                  originY: "center",
                  fontFamily: "monospace",
               })
               return ret
            },
            render_field: (obj, field_value, name, load_next, sw_write) => {
               obj.value.set({text: field_value})
               obj.label.set({fill: "black", text: name})
               if (load_next) {
                  obj.value.set({fill: "blue"})
                  if (sw_write) {
                     obj.action.set({fill: "black", text: "sw wr"})
                  } else {
                     obj.action.set({fill: "black", text: "hw wr"})
                  }
                  return `#77DD77`
               } else {
                  obj.value.set({fill: "black"})
                  obj.action.set({fill: "black", text: ""})
                  return `#F3F5A9`
               }
            },
            init_register: (words, box, label, value) => {
               ret = {}
               words.forEach((border, index) => {
                  ret["border" + index] = new fabric.Rect({
                     ...border,
                     stroke: "#AAAAAA",
                     fill: null,
                  })
               })
               ret.box = new fabric.Rect({
                  ...box,
                  strokeWidth: 1,
                  fill: "#F5A7A6",
                  stroke: "black",
                  rx: 8,
                  ry: 8,
               })
               ret.label = new fabric.Text("", {
                  ...label,
                  originX: "center",
                  originY: "center",
                  fontFamily: "monospace",
               })
               ret.value = new fabric.Text("", {
                  ...value,
                  originX: "center",
                  originY: "center",
                  fontFamily: "monospace",
               })
               return ret
            },
            render_register: (obj, name, register_size, register_value, number_of_words, load_nexts, fields, action_signals) => {
               let create_slot = (slot_top, slot_left, word) => {
                  let sw_write = action_signals[0].step(1).asInt() & action_signals[1].step(1).asInt()
                  let action = ""
                  if (sw_write) {
                     action = "sw wr"
                  } else {
                     action = "hw wr"
                  }
                  objects = []
                  objects.push(new fabric.Rect({
                     width: {{sizes.timeline_slot_width}},
                     height: {{sizes.timeline_slot_height}},
                     left: slot_left,
                     top: slot_top,
                     strokeWidth: 1,
                     fill: "#F3F5A9",
                     stroke: "#A9AB61",
                  }))
                  objects.push(new fabric.Rect({
                     width: {{sizes.timeline_slot_width}},
                     height: {{sizes.timeline_slot_height - sizes.timeline_slot_field_height}},
                     left: slot_left,
                     top: slot_top + {{sizes.timeline_slot_field_height}},
                     strokeWidth: 1,
                     fill: "#F3F5A9",
                     stroke: "#A9AB61",
                  }))
                  objects.push(new fabric.Text(action, {
                     fontSize: 10,
                     left: slot_left + {{sizes.timeline_slot_width/2}},
                     top: slot_top + {{sizes.timeline_slot_field_height + (sizes.timeline_slot_height - sizes.timeline_slot_field_height)/2}},
                     originX: "center",
                     originY: "center",
                     fontFamily: "monospace",
                  }))
                  fields[word].forEach((field, index) => {
                     let value = ""
                     if (field.width > 3) {
                        value = `${field.width}h''${field.value.step(1).asHexStr()}`
                     } else if (field.width > 1) {
                        value = `${field.width}b''${field.value.step(1).asBinaryStr()}`
                     } else {
                        value = field.value.step(1).asBinaryStr()
                     }
                     objects.push(new fabric.Rect({
                        width: field.width * {{sizes.timeline_slot_field_width}},
                        height: {{sizes.timeline_slot_field_height}},
                        left: slot_left + field.left * {{sizes.timeline_slot_field_width}},
                        top: slot_top,
                        strokeWidth: 1,
                        fill: "#F3F5A9",
                        stroke: "#A9AB61",
                     }))
                     objects.push(new fabric.Text(value, {
                        fontSize: 8,
                        left: slot_left + (field.left + field.width/2) * {{sizes.timeline_slot_field_width}},
                        top: slot_top + {{sizes.timeline_slot_field_height/2}},
                        originX: "center",
                        originY: "center",
                        fontFamily: "monospace",
                     }))
                  });
                  objects.push(new fabric.Rect({
                     width: {{sizes.timeline_slot_width}},
                     height: {{sizes.timeline_slot_height}},
                     left: slot_left,
                     top: slot_top,
                     strokeWidth: 1,
                     fill: "transparent",
                     stroke: "black",
                  }))
                  return objects
               }
               obj.label.set({fill: "black", text: name})
               obj.value.set({fill: "black", text: `${register_size}''h` + register_value})
               let ret = []
               for (let word = 0; word < number_of_words; word++) {
                  for (let i = 0; i < 51; i++) {
                     if (load_nexts[word].step(1).asBool()) {
                        ret.push(...create_slot(word * {{sizes.field_height}}, {{sizes.timeline_slot_width + sizes.timeline_spacing}} * i + {{sizes.timeline_left}}, word))
                     }
                  }
               }
               return ret
            },
            init_node: (box, label) => {
               ret = {}
               ret.box = new fabric.Rect({
                  ...box,
                  strokeWidth: 1,
                  stroke: "black",
                  rx: 8,
                  ry: 8,
               })
               ret.label = new fabric.Text("", {
                  ...label,
                  originX: "center",
                  originY: "center",
                  fontFamily: "monospace",
               })
               ret.label.rotate(-90)
               return ret
            }
         }
{{viz_code.get_all_lines()}}
{%- if module_content %}

\SV
endmodule
{% raw %}{% endraw %}
{{ module_content }}
{%- endif %}{# (eof newline anchor) #}