from typing import TYPE_CHECKING

from peakrdl.plugins.exporter import ExporterSubcommandPlugin
from exporter import VIZExporter
from peakrdl_regblock.udps import ALL_UDPS

if TYPE_CHECKING:
    import argparse
    from systemrdl.node import AddrmapNode

class Exporter(ExporterSubcommandPlugin):
    short_desc = "Generate a VIZ model for control/status register (CSR) visualization"

    udp_definitions = ALL_UDPS

    def add_exporter_arguments(self, arg_group: 'argparse.ArgumentParser') -> None:
        arg_group.add_argument(
            "--sv",
            action="store_true", 
            help="export System Verilog module with output"
        )

        arg_group.add_argument(
            "--tlv",
            action="store_true", 
            help="export TL-Verilog module with output"
        )

    def do_export(self, top_node: 'AddrmapNode', options: 'argparse.Namespace') -> None:
        x = VIZExporter()
        x.export(
            top_node,
            options.output,
            sv_flag = options.sv,
            tlv_flag = options.tlv
        )
