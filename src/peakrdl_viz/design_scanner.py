from systemrdl import RDLListener

class DesignScanner(RDLListener):

    def __init__(self) -> None:
        self.access_width: int = 8
        self.depth: int = 0
        self.max_depth: int = 1

    def enter_Reg(self, node) -> None:
        access_width = node.get_property('accesswidth')
        self.access_width = max(self.access_width, access_width)

    def enter_Component(self, node):
        self.depth += 1

    def enter_Field(self, node):
        self.max_depth = max(self.max_depth, self.depth)
    
    def exit_Component(self, node):
        self.depth -= 1