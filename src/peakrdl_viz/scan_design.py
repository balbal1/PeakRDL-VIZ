from systemrdl import RDLListener

class DesignScanner(RDLListener):

    def __init__(self) -> None:
        self.access_width = 8

    def enter_Reg(self, node) -> None:
        access_width = node.get_property('accesswidth')
        self.access_width = max(self.access_width, access_width)
