\m5_TLV_version 1d: tl-x.org
\SV
{% raw %}{% endraw %}
{%- if package_content %}
{{ package_content }}
{%- endif %}{% raw %}
\TLV ff(/_ff, _register, _field, #_index, #_x, #_y)
   /_ff
      \viz_js
         box: {width: 50, height: 40, strokeWidth: 1},
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
         render() {
            let objs = this.getObjects()
            {% endraw %}let field = this.sigVal(`{{ module_name }}.field_storage.${_register}.${_field}.value`){% raw %}
            objs.bit.set({text: field.getValue()[#_index]})
            objs.label.set({text: `${_field}[${#_index}]`})
            return []
         },
         where: {left: #_x * 50, top: #_y*80}
{% endraw %}
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

{{ff.get_flip_flops()}}

   *passed = *cyc_cnt > 20;
   *failed = 1'b0;

\SV
endmodule
{% raw %}{% endraw %}
{%- if package_content %}
{{ module_content }}
{%- endif %}{# (eof newline anchor) #}