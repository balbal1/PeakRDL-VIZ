\m5_TLV_version 1d: tl-x.org
{% raw %}{% endraw %}
{%- if package_content %}
\SV
{% raw %}{% endraw %}
{{ package_content }}
{%- endif %}{% raw %}
\TLV reg(/_reg, _register, #_index, #_x, #_y, #_width, #_height, _color)
   /_reg
      \viz_js
         box: {width: #_width, height: #_height, strokeWidth: 1},
         init() {
            let ret = {}
            ret.label = new fabric.Text("", {
               left: 0, top: -15,
               fontSize: 12, fontFamily: "Courier New",
            })
            return ret
         },
         renderFill() {
            let objs = this.getObjects()
            objs.label.set({text: `${_register}`})
            return `#_color`
         },
         where: {left: #_x, top: #_y}

\TLV ff(/_ff, _path, _field, #_index, #_x, #_y, #_width, #_height, _color)
   /_ff
      \viz_js
         box: {width: #_width, height: #_height, strokeWidth: 1},
         init() {
            let ret = {}
            ret.bit = new fabric.Text("", {
               left: 18, top: 7,
               fontSize: 22, fontFamily: "Courier New",
            })
            ret.label = new fabric.Text("", {
               left: 0, top: -15,
               fontSize: 6, fontFamily: "Courier New",
            })
            return ret
         },
         renderFill() {
            let objs = this.getObjects()
            {% endraw %}let field = this.sigVal(`{{ module_name }}.field_storage.${_path}.value`){% raw %}
            objs.bit.set({text: field.getValue()[#_index]})
            objs.label.set({text: `${_field}[${#_index}]`})
            return `#_color`
         },
         where: {left: #_x, top: #_y}

\TLV empty_ff(/_ff, #_x, #_y, #_width, #_height)
   /_ff
      \viz_js
         box: {width: #_width, height: #_height, strokeWidth: 1},
         renderFill() {
            return `#AAAAAA`
         },
         where: {left: #_x, top: #_y}
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

   {{ module_name }} {{ module_name }}($clk, $reset, $s_apb_psel, $s_apb_penable, $s_apb_pwrite, $s_apb_paddr, $s_apb_pwdata, $s_apb_pready, $s_apb_prdata, $s_apb_pslverr, *hwif_in, *hwif_out);
{% else %}
\TLV
{%- endif %}
{{ff.get_all_lines()}}
{%- if module_content %}

   *passed = *cyc_cnt > 20;
   *failed = 1'b0;

\SV
endmodule
{% raw %}{% endraw %}
{{ module_content }}
{%- endif %}{# (eof newline anchor) #}