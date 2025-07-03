import os
import jinja2 as jj
from typing import Union, Any

from systemrdl.node import AddressableNode, RootNode, Node
from systemrdl.node import AddrmapNode, MemNode
from systemrdl.node import RegNode, RegfileNode, FieldNode
from systemrdl import RDLCompiler, RDLCompileError, RDLWalker, RDLListener
from peakrdl_regblock import RegblockExporter
from peakrdl_regblock.cpuif.apb3 import APB3_Cpuif_flattened

from generator import GenerateFieldsVIZ
from scan_design import DesignScanner

class VIZExporter:

    def __init__(self, **kwargs: Any) -> None:
        # Check for stray kwargs
        if kwargs:
            raise TypeError(f"got an unexpected keyword argument '{list(kwargs.keys())[0]}'")

        loader = jj.ChoiceLoader([
            jj.FileSystemLoader(os.path.dirname(__file__)),
            jj.PrefixLoader({
                'base': jj.FileSystemLoader(os.path.dirname(__file__)),
            }, delimiter=":")
        ])

        self.jj_env = jj.Environment(
            loader=loader,
            undefined=jj.StrictUndefined,
        )

    def export(self, node: Union[AddrmapNode, RootNode], output_dir: str, **kwargs: Any) -> None:
        
        sv_flag: bool = kwargs.pop("sv_flag", False)
        tlv_flag: bool = kwargs.pop("tlv_flag", False)

        module_name: str = node.inst_name
        module_content: str = ""
        package_content: str = ""

        if tlv_flag:
            raise NotImplementedError

        if sv_flag:
            exporter = RegblockExporter()
            exporter.export(
                node, f"{output_dir}/temp_files",
                cpuif_cls=APB3_Cpuif_flattened
            )

            with open(f"{output_dir}/temp_files/{module_name}.sv", "r") as f:
                module_content = f.read()

            with open(f"{output_dir}/temp_files/{module_name}_pkg.sv", "r") as f:
                package_content = f.read()
        
        walker = RDLWalker(unroll=True)
        
        scan_listener = DesignScanner()
        walker.walk(node, scan_listener)

        generate_listener = GenerateFieldsVIZ(module_name, scan_listener.access_width)
        walker.walk(node, generate_listener)

        context = {
            "module_name": module_name,
            "access_width": scan_listener.access_width,
            "viz_code": generate_listener,
            "module_content": module_content,
            "package_content": package_content,
        }

        # Write out design
        template = self.jj_env.get_template("templates/viz_template.tlv")
        stream = template.stream(context)
        stream.dump(f"{output_dir}/{module_name}.tlv")

