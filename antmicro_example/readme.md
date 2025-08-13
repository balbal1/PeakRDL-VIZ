This is an example from [Antmicro's I3C project](https://github.com/antmicro/i3c-core)

To compile the RDL into SystemVerilog:

```peakrdl regblock antmicro_example/rdl/registers.rdl -o antmicro_example/output/temp_files --cpuif apb3-flat```

To generate the output TLV file with visualization:

```peakrdl viz -o antmicro_example/output antmicro/rdl/registers.rdl --sv-module antmicro/output/temp_files/I3CCSR.sv```