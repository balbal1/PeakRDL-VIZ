import math
import re
from typing import Union, Any

from systemrdl.node import AddressableNode, RootNode, Node
from systemrdl.node import AddrmapNode, MemNode
from systemrdl.node import RegNode, RegfileNode, FieldNode
from systemrdl import RDLCompiler, RDLCompileError, RDLWalker, RDLListener

from .design_scanner import DesignScanner

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

    SIZES = {
        1: {
            "FIELD_WIDTH": 50,
            "FIELD_HEIGHT": 70,
            "REGISTER_NODE_WIDTH": 90,
            "NODE_WIDTH": 50,
            "SPACING": 25,
            "BORDER_WIDTH": 10,
            "NODE_FONT_SIZE": 12,
            "REGISTER_FONT_SIZE": 12,
            "FIELD_LABEL_FONT_SIZE": [8, 12, 12],
            "FIELD_VALUE_FONT_SIZE": [22, 20, 20]
        },
        2: {
            "FIELD_WIDTH": 50,
            "FIELD_HEIGHT": 110,
            "REGISTER_NODE_WIDTH": 90,
            "NODE_WIDTH": 50,
            "SPACING": 25,
            "BORDER_WIDTH": 10,
            "NODE_FONT_SIZE": 12,
            "REGISTER_FONT_SIZE": 12,
            "FIELD_LABEL_FONT_SIZE": [8, 12, 12],
            "FIELD_VALUE_FONT_SIZE": [22, 20, 20]
        },
        4: {
            "FIELD_WIDTH": 50,
            "FIELD_HEIGHT": 130,
            "REGISTER_NODE_WIDTH": 350,
            "NODE_WIDTH": 100,
            "SPACING": 60,
            "BORDER_WIDTH": 10,
            "NODE_FONT_SIZE": 30,
            "REGISTER_FONT_SIZE": 25,
            "FIELD_LABEL_FONT_SIZE": [10, 20, 20],
            "FIELD_VALUE_FONT_SIZE": [46, 44, 44]
        },
        8: {
            "FIELD_WIDTH": 50,
            "FIELD_HEIGHT": 150,
            "REGISTER_NODE_WIDTH": 90,
            "NODE_WIDTH": 50,
            "SPACING": 25,
            "BORDER_WIDTH": 10,
            "NODE_FONT_SIZE": 12,
            "REGISTER_FONT_SIZE": 12,
            "FIELD_LABEL_FONT_SIZE": [8, 12, 12],
            "FIELD_VALUE_FONT_SIZE": [22, 20, 20]
        },
    }

    def __init__(self, node, module_name):

        walker = RDLWalker(unroll=True)
        
        scan_listener = DesignScanner()
        walker.walk(node, scan_listener)

        self.access_width = scan_listener.access_width
        self.access_width_bytes = math.ceil(self.access_width // 8)
        self.max_depth = scan_listener.max_depth
        self.module_name = module_name

        self.sizes = self.SIZES[self.access_width_bytes]

        self.level = 0
        self.code_indent = self.CODE_INDENT
        self.indent()

    def size_field(self, node: FieldNode):
        
        field_size = node.high - node.low + 1
        if field_size == 1:
            label_font_size = self.sizes["FIELD_LABEL_FONT_SIZE"][0]
            value_font_size = self.sizes["FIELD_VALUE_FONT_SIZE"][0]
            radix = ""
            radix_name = "Binary"
        elif field_size < 4:
            label_font_size = self.sizes["FIELD_LABEL_FONT_SIZE"][1]
            value_font_size = self.sizes["FIELD_VALUE_FONT_SIZE"][1]
            radix = f"{field_size}''b"
            radix_name = "Binary"
        else:
            label_font_size = self.sizes["FIELD_LABEL_FONT_SIZE"][2]
            value_font_size = self.sizes["FIELD_VALUE_FONT_SIZE"][2]
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
            "implements_storage": node.implements_storage,
            "width": field_size * self.sizes["FIELD_WIDTH"],
            "height": self.sizes["FIELD_HEIGHT"],
            "left": (self.access_width - (node.high % self.access_width) - 1) * self.sizes["FIELD_WIDTH"] + self.sizes["REGISTER_NODE_WIDTH"] + self.sizes["BORDER_WIDTH"] + self.sizes["SPACING"],
            "top": (node.high // self.access_width) * (self.sizes["FIELD_HEIGHT"] + self.sizes["BORDER_WIDTH"]) - self.sizes["BORDER_WIDTH"],
        }
        return properties
    
    def size_register(self, node: RegNode):
        fields_array = []
        for field in reversed(node.fields(include_gaps=True)):
            if isinstance(field, FieldNode):
                scope = self.standard_scope(field)
                fields_array.append(f"/{scope}$field_value")
            else:
                fields_array.append(f"{field[0] - field[1] + 1}'b{'0' * (field[0] - field[1] + 1)}")
        concat_fields = "{" + ', '.join(fields_array) + "}"

        no_of_words = math.ceil(node.size * 8 / self.access_width)
        words = []
        for i in range(no_of_words):
            words.append(i)

        properties = {
            "name": node.get_path_segment(),
            "path": ".".join(node.get_path_segments()[1:]),
            "indent": self.code_indent,
            "register_size": node.size * 8,
            "access_width": self.access_width,
            "words": words,
            "concat_fields": concat_fields,
            "register_width": self.access_width * self.sizes["FIELD_WIDTH"] + self.sizes["BORDER_WIDTH"],
            "register_height": self.sizes["FIELD_HEIGHT"] + self.sizes["BORDER_WIDTH"],
            "register_node_width": self.sizes["REGISTER_NODE_WIDTH"],
            "register_font_size": self.sizes["REGISTER_FONT_SIZE"],
            "border_width": self.sizes["BORDER_WIDTH"],
            "spacing": self.sizes["SPACING"],
            "height": math.ceil(node.size * 8 / self.access_width) * (self.sizes["FIELD_HEIGHT"] + self.sizes["BORDER_WIDTH"]) - 3 * self.sizes["BORDER_WIDTH"],
            "left": (self.max_depth - (self.code_indent/3) + 2) * (self.sizes["NODE_WIDTH"] + self.sizes["SPACING"]),
            "top": (node.address_offset * 8 // self.access_width) * (self.sizes["FIELD_HEIGHT"] + self.sizes["BORDER_WIDTH"]) - 2 * self.sizes["BORDER_WIDTH"],
        }
        return properties
        
    def size_node(self, node: Union[AddrmapNode, RegfileNode, MemNode]):
        properties = {
            "name": node.get_path_segment(),
            "indent": self.code_indent,
            "color": self.COLOR_CODES[node.__class__],
            "node_font_size": self.sizes["NODE_FONT_SIZE"],
            "spacing": self.sizes["NODE_WIDTH"] + self.sizes["SPACING"],
            "node_width": self.sizes["NODE_WIDTH"],
            "height": math.ceil(node.size * 8 / self.access_width) * (self.sizes["FIELD_HEIGHT"] + self.sizes["BORDER_WIDTH"]) - 3 * self.sizes["BORDER_WIDTH"],
            "top": (node.address_offset * 8 // self.access_width) * (self.sizes["FIELD_HEIGHT"] + self.sizes["BORDER_WIDTH"]) - 2 * self.sizes["BORDER_WIDTH"],
        }
        return properties

    def start_scope(self, node):
        scope = self.standard_scope(node)
        return self.code_indent * ' ' + f'/{scope}'

    def indent(self):
        self.level += 1
        self.code_indent += self.CODE_INDENT

    def outdent(self):
        self.level -= 1
        self.code_indent -= self.CODE_INDENT

    def standard_scope(self, node):
        # return node.get_path_segment().lower()
        return re.sub('_', 'd', re.sub('\d', 'd', node.get_path_segment().lower()))
