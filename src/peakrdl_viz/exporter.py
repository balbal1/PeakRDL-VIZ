import os
import jinja2 as jj
from typing import Union, Any

from systemrdl.node import AddressableNode, RootNode, Node
from systemrdl.node import AddrmapNode, MemNode
from systemrdl.node import RegNode, RegfileNode, FieldNode
from systemrdl import RDLWalker

from .Constants import Constants
from .generator import GenerateFieldsVIZ

class VIZExporter:

    def __init__(self, **kwargs: Any) -> None:
        # Check for stray kwargs
        if kwargs:
            raise TypeError(f"got an unexpected keyword argument '{list(kwargs.keys())[0]}'")

        self.jj_env = jj.Environment(
            loader = jj.FileSystemLoader(os.path.dirname(__file__)),
            undefined = jj.StrictUndefined,
        )

    def export(self, node: Union[AddrmapNode, RootNode], output_dir: str, **kwargs: Any) -> None:
        
        sv_module: str = kwargs.pop("sv_module", None)
        sv_package: str = kwargs.pop("sv_package", None)
        tlv_flag: bool = kwargs.pop("tlv_flag", False)
        root_path: bool = kwargs.pop("root_path", None)

        module_name: str = ""
        module_content: str = ""
        package_content: str = ""

        if tlv_flag:
            raise NotImplementedError

        if sv_module:
            try:
                with open(sv_module, "r") as f:
                    module_content = f.read()
            except FileNotFoundError:
                node.env.msg.fatal("Entered SystemVerilog module file does not exist.")

            if sv_package:
                try:
                    with open(sv_package, "r") as f:
                        package_content = f.read()
                except FileNotFoundError:
                    node.env.msg.fatal("Entered SystemVerilog package file does not exist.")
            else:
                sv_package = sv_module.replace(".sv", "_pkg.sv")
                try:
                    with open(sv_package, "r") as f:
                        package_content = f.read()
                except FileNotFoundError:
                    node.env.msg.fatal("Couldn't find SystemVerilog package file automatically, please specify the path using --sv-package.")
            module_name = node.inst_name
        else:
            if root_path:
                module_name = root_path

        walker = RDLWalker(unroll=True)
        
        generate_listener = GenerateFieldsVIZ(node, module_name, sv_module)
        walker.walk(node, generate_listener)

        context = {
            "module_name": module_name,
            "access_width": generate_listener.access_width,
            "viz_code": generate_listener,
            "sizes": Constants,
            "module_content": module_content,
            "package_content": package_content,
        }

        # Write out design
        template = self.jj_env.get_template("templates/viz_template.tlv")
        stream = template.stream(context)
        stream.dump(f"{output_dir}/{module_name}.tlv")

