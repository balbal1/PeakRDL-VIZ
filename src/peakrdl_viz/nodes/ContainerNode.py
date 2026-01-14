from systemrdl.node import AddressableNode, RootNode, Node
from systemrdl.node import AddrmapNode, MemNode
from systemrdl.node import RegNode, RegfileNode, FieldNode
from systemrdl import RDLCompiler, RDLCompileError, RDLWalker, RDLListener

import math
import re

from Constants import Constants
from helpers import standard_scope

class ContainerNode(RegfileNode):

    def __init__(self, container_node: AddressableNode):
        self.__dict__ = container_node.__dict__
        self.kind = container_node.__class__

    def number_of_words(self, size):
        return math.ceil(size / Constants.access_width_bytes)

    @property
    def name(self):
        return self.get_path_segment()
    
    @property
    def font_size(self):
        return Constants.NODE_FONT_SIZE
    
    @property
    def color(self):
        return Constants.COLOR_CODES[self.kind]
    
    @property
    def width(self):
        return Constants.NODE_WIDTH

    @property
    def spacing(self):
        return Constants.NODE_WIDTH + Constants.SPACING
    
    @property
    def top(self):
        if self.kind == AddrmapNode:
            return (self.absolute_address * 8 // Constants.access_width_bits) * (Constants.FIELD_HEIGHT + Constants.BORDER_WIDTH) - 2 * Constants.BORDER_WIDTH
        else:
            return ((self.absolute_address - Constants.base_address) * 8 // Constants.access_width_bits) * (Constants.FIELD_HEIGHT + Constants.BORDER_WIDTH) - 2 * Constants.BORDER_WIDTH
        
    @property
    def height(self):
        if self.kind == AddrmapNode:
            return self.number_of_words(self.size - Constants.base_address) * (Constants.FIELD_HEIGHT + Constants.BORDER_WIDTH) - 3 * Constants.BORDER_WIDTH
        else:
            return self.number_of_words(self.size) * (Constants.FIELD_HEIGHT + Constants.BORDER_WIDTH) - 3 * Constants.BORDER_WIDTH
