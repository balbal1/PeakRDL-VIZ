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
   /table_yy[{{viz_code.reg_base_address + 1}}:0]
      \viz_js
         box: {width: 400, height: 10, strokeWidth: 0},
         renderFill() {
            return `#AAAAAA`
         },
         where: {top: -10},
         layout: {top: 80}

   /table_border[1:0]
      \viz_js
         box: {width: 10, height: {{(viz_code.reg_base_address + 1) * 80 + 10}}, strokeWidth: 0},
         renderFill() {
            return `#AAAAAA`
         },
         where: {left: -10, top: -10},
         layout: {left: 410}

   /table_xx[{{access_width-2}}:0]
      \viz_js
         box: {width: 1, height: {{(viz_code.reg_base_address + 1) * 80}}, strokeWidth: 0},
         renderFill() {
            return `#AAAAAA`
         },
         where: {left: 49.5},
         layout: {left: 50}

{{viz_code.get_all_lines()}}
{%- if module_content %}

\SV
endmodule
{% raw %}{% endraw %}
{{ module_content }}
{%- endif %}{# (eof newline anchor) #}