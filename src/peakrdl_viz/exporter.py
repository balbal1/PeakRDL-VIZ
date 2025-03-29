import os
import jinja2 as jj
from typing import Union, Any

from systemrdl.node import AddressableNode, RootNode, Node
from systemrdl.node import AddrmapNode, MemNode
from systemrdl.node import RegNode, RegfileNode, FieldNode
from systemrdl import RDLCompiler, RDLCompileError, RDLWalker, RDLListener
from peakrdl_regblock import RegblockExporter
from peakrdl_regblock.cpuif.apb3 import APB3_Cpuif_flattened

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

    def export(self, node: Union[AddrmapNode, RootNode], sv_flag: bool, tlv_flag: bool) -> None:
        
        module_name: str = node.inst_name
        module_content: str = ""
        package_content: str = ""

        if tlv_flag:
            raise NotImplementedError

        if sv_flag:
            exporter = RegblockExporter()
            exporter.export(
                node, "temp_files",
                cpuif_cls=APB3_Cpuif_flattened
            )

            with open(f"temp_files/{module_name}.sv", "r") as f:
                module_content = f.read()

            with open(f"temp_files/{module_name}_pkg.sv", "r") as f:
                package_content = f.read()
        
        walker = RDLWalker(unroll=True)
        listener = GenerateFieldsVIZ()
        walker.walk(node, listener)

        context = {
            "module_name": module_name,
            "ff": listener,
            "module_content": module_content,
            "package_content": package_content,
        }

        # Write out design
        template = self.jj_env.get_template("viz_template.tlv")
        stream = template.stream(context)
        stream.dump(f"{module_name}.tlv")

    
class GenerateFieldsVIZ(RDLListener):
    def __init__(self) -> None:
        self.lines: list[str] = []
        self.indent: int = 0
        self.regcount: int = 0

    def enter_Component(self, node) -> None:
        if not isinstance(node, FieldNode):
            self.indent += 1
            self.regcount += 1

    def enter_Field(self, node) -> None:
        if "r" in node.get_property('hw').name:
            for bit in range(node.low, node.high+1):
                self.lines.append(f'   m5+ff(/{node.parent.get_path_segment().lower()}{bit}, "{node.parent.get_path_segment()}", "{node.get_path_segment()}", {bit-node.low}, {bit}, {self.regcount})')

    def exit_Component(self, node) -> None:
        if not isinstance(node, FieldNode):
            self.indent -= 1

    def get_flip_flops(self) -> str:
        return "\n".join(self.lines)
