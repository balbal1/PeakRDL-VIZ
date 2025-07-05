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
   
   $clk = *clk;
   $reset = *reset;
   $s_apb_pwrite = 1;

   {{ module_name }} {{ module_name }}($clk, $reset, $s_apb_psel, $s_apb_penable, $s_apb_pwrite, $s_apb_paddr[3:0], $s_apb_pwdata[{{access_width-1}}:0], $s_apb_pready, $s_apb_prdata[{{access_width-1}}:0], $s_apb_pslverr, *hwif_in, *hwif_out);

   *passed = *cyc_cnt > 100;
   *failed = 1'b0;
{% else %}
\TLV
{%- endif %}
   // /table
   //    \viz_js
   //       box: {width: {{access_width * 50 + 20}}, height: {{(viz_code.reg_base_address + 1) * 80 + 20}}, strokeWidth: 0},
   //       renderFill() {
   //          return `#AAAAAA`
   //       },
   //       where: {left: -10, top: -10}

   /top_viz
      \viz_js
         lib: {
            init_field: (width, label_font_size, value_font_size) => {
               let ret = {}
               ret.label = new fabric.Text("", {
                  top: 10,
                  left: width/2,
                  originX: "center",
                  originY: "center",
                  fontFamily: "monospace",
                  fontSize: label_font_size
               })
               ret.value = new fabric.Text("", {
                  top: 35,
                  left: width/2,
                  originX: "center",
                  originY: "center",
                  fontFamily: "monospace",
                  fontSize: value_font_size
               })
               ret.action = new fabric.Text("", {
                  top: 60,
                  left: width/2,
                  originX: "center",
                  originY: "center",
                  fontFamily: "monospace",
                  fontSize: label_font_size
               })
               return ret
            },
            render_field: (obj, field_value, name, load_next, sw_write) => {
               obj.value.set({text: field_value})
               obj.label.set({fill: "black", text: name})
               if (load_next) {
                  obj.value.set({fill: "blue"})
                  if (sw_write) {
                     obj.action.set({fill: "black", text: "sw write"})
                  } else {
                     obj.action.set({fill: "black", text: "hw write"})
                  }
                  return `#77DD77`
               } else {
                  obj.value.set({fill: "black"})
                  obj.action.set({fill: "black", text: ""})
                  return `#F3F5A9`
               }
            },
            init_register: (height, no_of_words, access_width) => {
               ret = {}
               ret.box = new fabric.Rect({
                  width: 90,
                  height: height,
                  fill: "#F5A7A6",
                  rx: 8,
                  ry: 8,
                  stroke: "black",
                  strokeWidth: 1,
               })
               for (let i = 0; i < no_of_words; i++) {
                  ret["border" + i] = new fabric.Rect({
                     width: access_width * 50 + 10,
                     height: 80,
                     left: 110,
                     top: i * 80 - 20,
                     fill: null,
                     stroke: "#AAAAAA",
                     strokeWidth: 10
                  })
               }
               ret.label = new fabric.Text("", {
                  top: height/2-10,
                  left: 45,
                  originX: "center",
                  originY: "center",
                  fontFamily: "monospace",
                  fontSize: 12
               })
               ret.value = new fabric.Text("", {
                  top: height/2+10,
                  left: 45,
                  originX: "center",
                  originY: "center",
                  fontFamily: "monospace",
                  fontSize: 12
               })
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