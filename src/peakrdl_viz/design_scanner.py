import math

from systemrdl import RDLListener

class DesignScanner(RDLListener):

    def __init__(self) -> None:
        self.access_width: int = 8
        self.depth: int = 0
        self.max_depth: int = 1
        self.max_address: int = 0
        self.base_address: int = None

    def enter_Reg(self, node) -> None:
        access_width = node.get_property('accesswidth')
        self.access_width = max(self.access_width, access_width)
        self.max_address = node.raw_address_offset
        if not self.base_address:
            self.base_address = node.raw_absolute_address

    def enter_Component(self, node):
        self.depth += 1

    def enter_Field(self, node):
        self.max_depth = max(self.max_depth, self.depth)
    
    def exit_Component(self, node):
        self.depth -= 1

    def get_address_space(self):
        return int(math.log2(self.max_address))