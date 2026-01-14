from systemrdl.node import AddressableNode, RootNode, Node
from systemrdl.node import AddrmapNode, MemNode
from systemrdl.node import RegNode, RegfileNode, FieldNode
from systemrdl import RDLCompiler, RDLCompileError, RDLWalker, RDLListener

import math
import re

from Constants import Constants
from helpers import standard_scope

class Register(RegNode):

    def __init__(self, register_node: RegNode, level: int):
        self.__dict__ = register_node.__dict__
        self.level = level

        self.words_array = []
        self.fields_array = []
        self.load_nexts_array = []
        self.fields_slot_array = []
        for i in range(self.no_of_words):
            self.words_array.append(i)
            self.load_nexts_array.append([])
            self.fields_slot_array.append([])

    def populate_fields(self, module_name, sv_flag):
        for field in reversed(self.fields(include_gaps=True)):
            if isinstance(field, FieldNode):
                # if field.implements_storage:
                scope = standard_scope(field)
                if (sv_flag):
                    self.fields_slot_array[field.low//Constants.access_width_bits].append({
                        "value": f"/{scope}$field_value",
                        "left": Constants.access_width_bits - (field.high % Constants.access_width_bits) - 1,
                        "width": field.width
                    })
                elif (not self.external and field.implements_storage):
                    self.fields_slot_array[field.low//Constants.access_width_bits].append({
                        "value": f"this.sigVal(`{module_name}.field_storage.{self.path}.{field.inst_name}.value`)",
                        "left": Constants.access_width_bits - (field.high % Constants.access_width_bits) - 1,
                        "width": field.width
                    })
                self.fields_array.append(f"/{scope}$field_value")
                self.load_nexts_array[field.low//Constants.access_width_bits].append(f"/{scope}$load_next")
                # else:
                #     fields_array.append(f"{field.width}'b{'0' * (field.width)}")
            else:
                self.fields_array.append(f"{field[0] - field[1] + 1}'b{'0' * (field[0] - field[1] + 1)}")

    @property
    def no_of_words(self):
        return math.ceil(self.size / Constants.access_width_bytes)

    @property
    def size_bits(self):
        return self.size * 8

    @property
    def font_size(self):
        return Constants.REGISTER_FONT_SIZE

    @property
    def name(self):
        return self.get_path_segment()

    @property
    def path(self):
        return ".".join(self.get_path_segments()[1:])

    @property
    def width(self):
        return Constants.REGISTER_NODE_WIDTH
    
    @property
    def height(self):
        return math.ceil(self.size_bits / Constants.access_width_bits) * (Constants.WORD_HEIGHT) - 3 * Constants.BORDER_WIDTH
    
    @property
    def left(self):
        return self.level * (Constants.NODE_WIDTH + Constants.SPACING)

    @property
    def top(self):
        return (self.address_offset * 8 // Constants.access_width_bits) * (Constants.WORD_HEIGHT) - 2 * Constants.BORDER_WIDTH

    @property
    def fields_values(self):
        return "{" + ', '.join(self.fields_array) + "}"
    
    @property
    def load_nexts(self):
        load_nexts = []
        for load_next in self.load_nexts_array:
            load_nexts.append("||".join(load_next))
        return load_nexts
    
    @property
    def fields_slot(self):
        return re.sub(r"'(this[^']*)'", r"\1", str(self.fields_slot_array).replace("'value'", "value").replace("'left'", "left").replace("'width'", "width"))
    
    @property
    def word_width(self):
        return Constants.WORD_WIDTH

    @property
    def word_height(self):
        return Constants.WORD_HEIGHT
    
    @property
    def border_width(self):
        return Constants.BORDER_WIDTH
    
    @property
    def spacing(self):
        return Constants.SPACING