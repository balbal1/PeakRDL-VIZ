import math
import re
from typing import Union, Any

from systemrdl.node import AddressableNode, RootNode, Node
from systemrdl.node import AddrmapNode, MemNode
from systemrdl.node import RegNode, RegfileNode, FieldNode
from systemrdl import RDLCompiler, RDLCompileError, RDLWalker, RDLListener

from .design_scanner import DesignScanner
from .sizes import Size

class DesignSizer:

    CODE_INDENT = 3

    COLOR_CODES = {
        AddrmapNode: "D0E4EE",
        MemNode: "D5D1E9",
        RegfileNode: "F5CF9F",
        RegNode: "F5A7A6",
        FieldNode: "F3F5A9",
        "BLANK": "AAAAAA"
    }

    def __init__(self, node, module_name):

        walker = RDLWalker(unroll=True)
        
        scan_listener = DesignScanner()
        walker.walk(node, scan_listener)

        self.access_width = scan_listener.access_width
        self.access_width_bytes = math.ceil(self.access_width // 8)
        self.max_depth = scan_listener.max_depth
        self.module_name = module_name
        self.max_address = scan_listener.get_address_space()
        self.base_address = scan_listener.base_address

        self.sizes = Size(self.access_width)

        self.level = 0
        self.field_number = 0
        self.code_indent = self.CODE_INDENT
        self.number_of_time_slots = 51
        self.indent()

    def size_field(self, node: FieldNode):

        field_size = node.high - node.low + 1
        if field_size == 1:
            label_font_size = self.sizes.field_label_font_size[0]
            value_font_size = self.sizes.field_value_font_size[0]
            radix = ""
            radix_name = "Binary"
        elif field_size < 4:
            label_font_size = self.sizes.field_label_font_size[1]
            value_font_size = self.sizes.field_value_font_size[1]
            radix = f"{field_size}''b"
            radix_name = "Binary"
        else:
            label_font_size = self.sizes.field_label_font_size[2]
            value_font_size = self.sizes.field_value_font_size[2]
            radix = f"{field_size}''h"
            radix_name = "Hex"
        
        properties = {
            "name": node.get_path_segment(),
            "path": ".".join(node.get_path_segments()[1:]),
            "module_name": self.module_name,
            "indent": self.code_indent,
            "field_size": field_size,
            "label_font_size": label_font_size,
            "value_font_size": value_font_size,
            "radix": radix,
            "radix_long": radix_name,
            "implements_storage": node.implements_storage and not node.external,
            "width": field_size * self.sizes.field_width,
            "height": self.sizes.field_height,
            "left": (self.access_width - (node.high % self.access_width) - 1) * self.sizes.field_width + self.sizes.register_node_width + self.sizes.border_width + self.sizes.spacing,
            "top": (node.high // self.access_width) * (self.sizes.field_height + self.sizes.border_width) - self.sizes.border_width,
        }
        return properties
    
    def size_register(self, node: RegNode):

        words = []
        fields_array = []
        load_next_array = []
        fields_slot = []
        no_of_words = self.sizes.get_no_of_words(node.size)
        for i in range(no_of_words):
            words.append(i)
            load_next_array.append([])
            fields_slot.append([])

        for field in reversed(node.fields(include_gaps=True)):
            if isinstance(field, FieldNode):
                # if field.implements_storage:
                scope = self.standard_scope(field)
                fields_slot[field.low//self.access_width].append({
                    "value": f"/{scope}$field_value",
                    "left": self.access_width - (field.high % self.access_width) - 1,
                    "width": field.width
                })
                fields_array.append(f"/{scope}$field_value")
                load_next_array[field.low//self.access_width].append(f"/{scope}$load_next")
                # else:
                #     fields_array.append(f"{field.width}'b{'0' * (field.width)}")
            else:
                fields_array.append(f"{field[0] - field[1] + 1}'b{'0' * (field[0] - field[1] + 1)}")
        concat_fields = "{" + ', '.join(fields_array) + "}"
        concat_load_next = []
        for load_next in load_next_array:
            concat_load_next.append("||".join(load_next))
        fields_slot_string = str(fields_slot).replace("'value'", "value").replace("'left'", "left").replace("'width'", "width")

        properties = {
            "name": node.get_path_segment(),
            "path": ".".join(node.get_path_segments()[1:]),
            "module_name": self.module_name,
            "indent": self.code_indent,
            "register_size": node.size * 8,
            "access_width": self.access_width,
            "words": words,
            "fields_slot": fields_slot_string,
            "concat_fields": concat_fields,
            "concat_load_next": concat_load_next,
            "register_width": self.access_width * self.sizes.field_width + self.sizes.border_width,
            "register_height": self.sizes.field_height + self.sizes.border_width,
            "register_node_width": self.sizes.register_node_width,
            "register_font_size": self.sizes.register_font_size,
            "border_width": self.sizes.border_width,
            "spacing": self.sizes.spacing,
            "height": math.ceil(node.size * 8 / self.access_width) * (self.sizes.field_height + self.sizes.border_width) - 3 * self.sizes.border_width,
            "left": (self.max_depth - (self.code_indent/3) + 2) * (self.sizes.node_width + self.sizes.spacing),
            "top": (node.address_offset * 8 // self.access_width) * (self.sizes.field_height + self.sizes.border_width) - 2 * self.sizes.border_width,
        }
        return properties
        
    def size_node(self, node: Union[AddrmapNode, RegfileNode, MemNode]):
        if isinstance(node, AddrmapNode):
            top = node.absolute_address
            height = self.sizes.get_node_height(node.size - self.base_address)
        else:
            top = node.absolute_address - self.base_address
            height = self.sizes.get_node_height(node.size)
        properties = {
            "name": node.get_path_segment(),
            "indent": self.code_indent,
            "color": self.COLOR_CODES[node.__class__],
            "node_font_size": self.sizes.node_font_size,
            "spacing": self.sizes.node_width + self.sizes.spacing,
            "node_width": self.sizes.node_width,
            "height": height,
            "top": (top * 8 // self.access_width) * (self.sizes.field_height + self.sizes.border_width) - 2 * self.sizes.border_width,
        }
        return properties

    def size_timeline(self):
        properties = {
            "width": (self.sizes.timeline_slot_width + self.sizes.timeline_spacing) * self.number_of_time_slots - self.sizes.timeline_spacing,
            "header_height": self.sizes.timeline_header_height,
            "font_size": 22,
            "slot_width": self.sizes.timeline_slot_width,
            "top": -2 * self.sizes.timeline_header_height,
            "left": self.access_width * self.sizes.field_width + (self.max_depth) * (self.sizes.node_width + self.sizes.spacing) + self.sizes.register_node_width,
            "spacing": self.sizes.timeline_slot_width + self.sizes.timeline_spacing,
        }
        return properties

    def start_scope(self, node):
        scope = self.standard_scope(node)
        return self.code_indent * ' ' + f'/{scope}'
    
    def randomize_field(self, node: FieldNode):
        lines = []
        if node.is_hw_writable and node.is_hw_readable and node.is_sw_writable and node.is_sw_readable:
            field_size = node.high - node.low
            lines.append(f"   *hwif_in.{'.'.join(node.get_path_segments()[1:])}.next = $rand{self.field_number}{f'[{field_size}:0];' if field_size > 0 else ';'}")
            # if node.get_property("hwenable"):
            if node.is_hw_readable and node.is_hw_writable:
                lines.append(f"   *hwif_in.{'.'.join(node.get_path_segments()[1:])}.we = $rand{self.field_number+1};")
        self.field_number += 2
        return lines


    def indent(self):
        self.level += 1
        self.code_indent += self.CODE_INDENT

    def outdent(self):
        self.level -= 1
        self.code_indent -= self.CODE_INDENT

    def standard_scope(self, node):
        # return node.get_path_segment().lower()
        text = node.get_path_segment().lower() + "_" + node.__class__.__name__[0].lower()
        text = re.sub(r"(\d+)(?=[A-Za-z])", 'd', text)
        text = re.sub(r"_(?=\d)", "_d", text)
        text = re.sub(r"_+", "_", text)
        text = re.sub(r"^_+", "", text)
        if re.match(r"^[A-Za-z](?:\d|_)", text):
            text = "d" + text
        return text
