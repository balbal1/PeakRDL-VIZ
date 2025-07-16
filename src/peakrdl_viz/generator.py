import jinja2 as jj

from systemrdl.node import AddressableNode, RootNode, Node
from systemrdl.node import AddrmapNode, MemNode
from systemrdl.node import RegNode, RegfileNode, FieldNode
from systemrdl import RDLListener

class GenerateFieldsVIZ(RDLListener):

    def __init__(self, design_sizer) -> None:
        self.jj_env = jj.Environment(
            loader = jj.PackageLoader("peakrdl_viz", "templates"),
            undefined= jj.StrictUndefined,
        )
        self.field_template = self.jj_env.get_template("field_template.tlv")
        self.register_template = self.jj_env.get_template("register_template.tlv")
        self.node_template = self.jj_env.get_template("node_template.tlv")

        self.design_sizer = design_sizer

        self.lines: list[str] = []
        self.hw_randomization: list[str] = []

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

        if node.is_hw_writable and node.is_hw_readable and node.is_sw_writable and node.is_sw_readable:
            field_size = node.high - node.low
            self.hw_randomization.append(f"   *hwif_in.{'.'.join(node.get_path_segments()[1:])}.next = $rand{len(self.hw_randomization)}{f'[{field_size}:0];' if field_size > 0 else ';'}")
            self.hw_randomization.append(f"   *hwif_in.{'.'.join(node.get_path_segments()[1:])}.we = $rand{len(self.hw_randomization)};")

    def exit_Component(self, node) -> None:
        self.design_sizer.outdent()

    def get_all_lines(self) -> str:
        return "\n".join(self.lines)

    def get_hw_randomization_lines(self):
        return "\n".join(self.hw_randomization)