import os
import jinja2 as jj
import math

from systemrdl.node import AddrmapNode, MemNode
from systemrdl.node import RegNode, RegfileNode, FieldNode
from systemrdl import RDLWalker, RDLListener

from .scanner import DesignScanner
from .Constants import Constants
from .helpers import standard_scope, randomize_field
from .nodes.Field import Field
from .nodes.Register import Register
from .nodes.ContainerNode import ContainerNode
from .nodes.Timeline import Timeline

class GenerateFieldsVIZ(RDLListener):

    CODE_INDENT = 3

    def __init__(self, node, module_name, sv_module) -> None:

        walker = RDLWalker(unroll=True)
        scan_listener = DesignScanner()
        walker.walk(node, scan_listener)

        self.sv_flag = sv_module is not None
        self.access_width = scan_listener.access_width
        self.access_width_bytes = math.ceil(self.access_width // 8)
        self.max_depth = scan_listener.max_depth
        self.module_name = module_name
        self.max_address = scan_listener.get_address_space()
        self.base_address = scan_listener.base_address

        Constants.set_access_width(self.access_width)
        Constants.set_base_address(self.base_address)
        Constants.set_max_depth(self.max_depth)
        Constants.set_constants()

        self.level = 0
        self.code_indent = self.CODE_INDENT
        self.number_of_time_slots = 51
        self.indent()


        self.jj_env = jj.Environment(
            loader = jj.FileSystemLoader(os.path.dirname(__file__)),
            undefined = jj.StrictUndefined,
        )
        self.timeline_template = self.jj_env.get_template("templates/timeline_template.tlv")
        self.field_template = self.jj_env.get_template("templates/field_template.tlv")
        self.register_template = self.jj_env.get_template("templates/register_template.tlv")
        self.node_template = self.jj_env.get_template("templates/node_template.tlv")

        self.lines: list[str] = []
        self.hw_randomization: list[str] = []

        self.timeline_lines = []
        timeline = Timeline()
        properties = {
            "timeline": timeline,
        }
        stream = self.timeline_template.render(properties).strip('\n')
        self.timeline_lines.append(stream)

    def enter_Component(self, node) -> None:
        scope = standard_scope(node)
        scope_line = self.code_indent * ' ' + f'/{scope}'
        self.lines.append(scope_line)
        self.indent()

        if isinstance(node, (AddrmapNode, RegfileNode, MemNode)):
            node = ContainerNode(node)
            properties = {
                "node": node,
                "indent": self.code_indent,
            }
            stream = self.node_template.render(properties).strip('\n')
            self.lines.append(stream)

    def enter_Reg(self, node) -> None:
        level = self.max_depth - self.level + 1
        node = Register(node, level)
        node.populate_fields(self.module_name, self.sv_flag)
        properties = {
            "node": node,
            "module_name": self.module_name,
            "indent": self.code_indent,
            "access_width": self.access_width,
            "sv_flag": self.sv_flag,
        }
        stream = self.register_template.render(properties).strip('\n')
        self.lines.append(stream)

    def enter_Field(self, node) -> None:
        node = Field(node)
        properties = {
            "node": node,
            "module_name": self.module_name,
            "indent": self.code_indent,
            "sv_flag": self.sv_flag,
        }
        stream = self.field_template.render(properties).strip('\n')
        self.lines.append(stream)

        hw_randomize_lines = randomize_field(node)
        self.hw_randomization.extend(hw_randomize_lines)

    def exit_Component(self, node) -> None:
        self.outdent()

    def get_all_lines(self) -> str:
        return "\n".join(self.lines)

    def get_hw_randomization_lines(self):
        return "\n".join(self.hw_randomization)

    def get_timeline_lines(self):
        return "\n".join(self.timeline_lines)

    def indent(self):
        self.level += 1
        self.code_indent += self.CODE_INDENT

    def outdent(self):
        self.level -= 1
        self.code_indent -= self.CODE_INDENT
