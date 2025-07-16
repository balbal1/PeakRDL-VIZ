from typing import TYPE_CHECKING

from peakrdl.plugins.exporter import ExporterSubcommandPlugin

from .exporter import VIZExporter

if TYPE_CHECKING:
    import argparse
    from systemrdl.node import AddrmapNode

class Exporter(ExporterSubcommandPlugin):
    short_desc = "Generate a VIZ model for control/status register (CSR) visualization"
    
    def add_exporter_arguments(self, arg_group: 'argparse.ArgumentParser') -> None:

        arg_group.add_argument(
            "--sv-module",
            metavar="NAME",
            default=None,
            help="SystemVerilog module file path"
        )

        arg_group.add_argument(
            "--sv-package",
            metavar="NAME",
            default=None,
            help="SystemVerilog package file path"
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
            sv_module = options.sv_module,
            sv_package = options.sv_package,
            tlv_flag = options.tlv
        )
