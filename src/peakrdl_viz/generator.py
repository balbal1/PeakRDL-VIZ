import os
import jinja2 as jj

from systemrdl.node import AddressableNode, RootNode, Node
from systemrdl.node import AddrmapNode, MemNode
from systemrdl.node import RegNode, RegfileNode, FieldNode
from systemrdl import RDLCompiler, RDLCompileError, RDLWalker, RDLListener

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

    def __init__(self, module_name, access_width) -> None:
        self.reg_lines: list[str] = []
        self.ff_lines: list[str] = []
        
        self.x_pointer: int = 0
        self.y_pointer: int = 0

        # stores the starting x and y positions of parent blocks
        self.x_stack: list[int] = [0]
        self.y_stack: list[int] = [0]
        self.width_stack: list[int] = [0]

        self.ff_visited: list[int] = []


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

        self.lines: list[str] = []
        self.reg_base_address: int
        self.code_indent: int = 3
        self.field_template = self.jj_env.get_template("templates/field_template.tlv")
        self.register_template = self.jj_env.get_template("templates/register_template.tlv")
        self.module_name = module_name
        self.access_width = access_width

    def enter_Component(self, node) -> None:
        self.lines.append(self.code_indent * ' ' + f'/{node.get_path_segments()[-1].lower()}')
        self.code_indent += 3

    def enter_Reg(self, node) -> None:
        self.reg_base_address = node.absolute_address
        context = {
            "name": node.get_path_segment(),
            "path": ".".join(node.get_path_segments()[1:]),
            "module_name": self.module_name,
            "indent": self.code_indent,
            "register_size": node.size * 8,
            "height": 80 * node.size - 30,
            "left": 500,
            "top": self.reg_base_address * 80 + 10,
        }
        stream = self.register_template.render(context).strip('\n')
        self.lines.append(stream)

    def enter_Field(self, node) -> None:
        field_size = node.high - node.low + 1
        context = {
            "name": node.get_path_segment(),
            "path": ".".join(node.get_path_segments()[1:]),
            "module_name": self.module_name,
            "indent": self.code_indent,
            "field_size": field_size,
            "label_font_size": 8 if field_size == 1 else 12,
            "value_font_size": 14 if field_size == 1 else 16,
            "radix": "b" if field_size < 4 else "h",
            "radix_long": "Binary" if field_size < 4 else "Hex",
            "width": field_size * 50,
            "left": (self.access_width - (node.high % self.access_width) - 1) * 50,
            "top": (node.high // self.access_width) * 80,
        }

        stream = self.field_template.render(context).strip('\n')
        self.lines.append(stream)

    def exit_Component(self, node) -> None:
        self.code_indent -= 3

    def get_all_lines(self) -> str:
        return "\n".join(self.lines)
