import os
import jinja2 as jj

from systemrdl.node import AddressableNode, RootNode, Node
from systemrdl.node import AddrmapNode, MemNode
from systemrdl.node import RegNode, RegfileNode, FieldNode
from systemrdl import RDLListener

class GenerateFieldsVIZ(RDLListener):

    def __init__(self, design_sizer) -> None:
        self.jj_env = jj.Environment(
            loader = jj.FileSystemLoader(os.path.dirname(__file__)),
            undefined = jj.StrictUndefined,
        )
        self.timeline_template = self.jj_env.get_template("templates/timeline_template.tlv")
        self.field_template = self.jj_env.get_template("templates/field_template.tlv")
        self.register_template = self.jj_env.get_template("templates/register_template.tlv")
        self.node_template = self.jj_env.get_template("templates/node_template.tlv")

        self.design_sizer = design_sizer

        self.lines: list[str] = []
        self.hw_randomization: list[str] = []

        self.timeline_lines = []
        context = self.design_sizer.size_timeline()
        stream = self.timeline_template.render(context).strip('\n')
        self.timeline_lines.append(stream)

    def enter_Component(self, node) -> None:
        scope_line = self.design_sizer.start_scope(node)
        self.lines.append(scope_line)
        self.design_sizer.indent()

        if isinstance(node, (AddrmapNode, RegfileNode, MemNode)):
            context = self.design_sizer.size_node(node)
            stream = self.node_template.render(context).strip('\n')
            self.lines.append(stream)

    def enter_Reg(self, node) -> None:
        context = self.design_sizer.size_register(node)
        stream = self.register_template.render(context).strip('\n')
        self.lines.append(stream)

    def enter_Field(self, node) -> None:
        context = self.design_sizer.size_field(node)
        stream = self.field_template.render(context).strip('\n')
        self.lines.append(stream)

        hw_randomize_lines = self.design_sizer.randomize_field(node)
        self.hw_randomization.extend(hw_randomize_lines)

    def exit_Component(self, node) -> None:
        self.design_sizer.outdent()

    def get_all_lines(self) -> str:
        return "\n".join(self.lines)

    def get_hw_randomization_lines(self):
        return "\n".join(self.hw_randomization)

    def get_timeline_lines(self):
        return "\n".join(self.timeline_lines)