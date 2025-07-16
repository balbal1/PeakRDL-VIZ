# PeakRDL_VIZ

This PeakRDL plugin exports VIZ code for visualizing SystemRDL files contents on MakerChip's online platform.

## Installing

```python3 -m pip install peakrdl-viz```

## How to use

for a quick test for the plugin:

```peakrdl viz -o output_files test_files/long_test.rdl --sv-module [path_to_generated_sv_module]```

import the output .tlv file (inside output_files) to makerchip and test

## Documentation

For more info, read the [documentation](https://peakrdl-viz.readthedocs.io/en/latest/)