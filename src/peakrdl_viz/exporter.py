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
        stream.dump(f"{output_dir}/{module_name}.tlv")

class GenerateFieldsVIZ(RDLListener):

    FF_WIDTH: int = 50
    FF_HEIGHT: int = 40
    X_INDENT: int = 20
    Y_INDENT: int = 10
    SPACING: int = 20
    TEXT_HEIGHT: int = 15

    COLOR_CODES = {
        AddrmapNode: "D0E4EE",
        MemNode: "D5D1E9",
        RegfileNode: "F5CF9F",
        RegNode: "F5A7A6",
        FieldNode: "F3F5A9",
        "blank": "AAAAAA"
    }

    def __init__(self) -> None:
        self.reg_lines: list[str] = []
        self.ff_lines: list[str] = []
        
        self.x_pointer: int = 0
        self.y_pointer: int = 0

        # stores the starting x and y positions of parent blocks
        self.x_stack: list[int] = [0]
        self.y_stack: list[int] = [0]
        self.width_stack: list[int] = [0]

        self.ff_visited: list[int] = []

    def enter_Component(self, node) -> None:
        if not isinstance(node, FieldNode):
            # add indent for a new level and save the start point in the stack
            self.x_pointer += self.X_INDENT
            self.x_stack.append(self.x_pointer)
            self.y_pointer += self.Y_INDENT + self.SPACING
            self.y_stack.append(self.y_pointer)
            self.width_stack.append(0)
            if isinstance(node, RegNode):
                self.ff_visited = []

    def enter_Field(self, node) -> None:
        if node.is_hw_readable:
            for bit in range(node.low, node.high + 1):
                self.ff_visited.append(bit)
                self.ff_lines.append(
                    f'   m5+ff('
                        f'/{node.get_path("_").lower()}{bit}, '
                        f'"{".".join(node.get_path_segments()[1:])}", '
                        f'"{node.get_path_segment()}", '
                        f'{bit - node.low}, '
                        f'{self.x_pointer + bit * self.FF_WIDTH + self.X_INDENT}, '
                        f'{self.y_pointer + self.Y_INDENT + self.TEXT_HEIGHT}, '
                        f'{self.FF_WIDTH}, '
                        f'{self.FF_HEIGHT}, '
                        f'{self.COLOR_CODES[node.__class__]}'
                    ')'
                )

    def exit_Component(self, node) -> None:
        if isinstance(node, RegNode):
            # draw all unused flip flops of the current register
            for bit in range(node.size * 8):
                if bit in self.ff_visited:
                    continue
                self.ff_lines.append(
                    f'   m5+empty_ff('
                        f'/{node.get_path("_").lower()}{bit}, '
                        f'{self.x_pointer + bit * self.FF_WIDTH + self.X_INDENT}, '
                        f'{self.y_pointer + self.Y_INDENT + self.TEXT_HEIGHT}, '
                        f'{self.FF_WIDTH}, '
                        f'{self.FF_HEIGHT}'
                    ')'
                )

        if not isinstance(node, FieldNode):
            # update the position pointers to include the block width and height
            self.x_pointer += 2 * self.X_INDENT
            self.y_pointer += 2 * self.Y_INDENT + self.TEXT_HEIGHT
            if isinstance(node, RegNode):
                self.y_pointer += self.FF_HEIGHT
                self.x_pointer += self.FF_WIDTH * node.size * 8

            x_pos: int = self.x_stack.pop(-1)
            y_pos: int = self.y_stack.pop(-1)

            # keep track of the maximum width of the current block
            self.width_stack[-1] = max(self.x_pointer - x_pos, self.width_stack[-1])
            self.x_pointer = self.x_stack[-1]

            # pop the current block width and propagate the width to its parent block
            width: int = self.width_stack.pop(-1)
            self.width_stack[-1] = max(width + 2 * self.X_INDENT, self.width_stack[-1])
            
            # draw current block
            self.reg_lines.append(
                f'   m5+reg('
                    f'/{node.get_path("_").lower()}, '
                    f'"{node.get_path_segment()}", '
                    f'{0}, '
                    f'{x_pos}, '
                    f'{y_pos}, '
                    f'{width}, '
                    f'{self.y_pointer - y_pos}, '
                    f'{self.COLOR_CODES[node.__class__]}'
                ')'
            )

    def get_all_lines(self) -> str:
        return "\n".join(reversed(self.reg_lines)) + "\n" + "\n".join(self.ff_lines)
