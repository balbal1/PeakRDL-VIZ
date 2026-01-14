from systemrdl.node import FieldNode

from Constants import Constants

class Field(FieldNode):

    def __init__(self, field_node: FieldNode):
        self.__dict__ = field_node.__dict__

    @property
    def spaceview_width(self):
        return self.width * Constants.FIELD_WIDTH
    
    @property
    def spaceview_height(self):
        return Constants.FIELD_HEIGHT
    
    @property
    def label_font_size(self):
        if self.width == 1:
            return Constants.FIELD_LABEL_FONT_SIZE[0]
        elif self.width < 4:
            return Constants.FIELD_LABEL_FONT_SIZE[1]
        else:
            return Constants.FIELD_LABEL_FONT_SIZE[2]
        
    @property
    def value_font_size(self):
        if self.width == 1:
            return Constants.FIELD_VALUE_FONT_SIZE[0]
        elif self.width < 4:
            return Constants.FIELD_VALUE_FONT_SIZE[1]
        else:
            return Constants.FIELD_VALUE_FONT_SIZE[2]
        
    @property
    def radix(self):
        if self.width == 1:
            return ""
        elif self.width < 4:
            return f"{self.width}''b"
        else:
            return f"{self.width}''h"
        
    @property
    def radix_name(self):
        if self.width < 4:
            return "Binary"
        else:
            return "Hex"
        
    @property
    def name(self):
        return self.get_path_segment()
    
    @property
    def path(self):
        return ".".join(self.get_path_segments()[1:])
    
    @property
    def value_exists(self):
        return self.implements_storage and not self.external
    
    @property
    def left(self):
        return (Constants.access_width_bits - (self.high % Constants.access_width_bits) - 1) * Constants.FIELD_WIDTH + Constants.REGISTER_NODE_WIDTH + Constants.BORDER_WIDTH + Constants.SPACING
    
    @property
    def top(self):
        return (self.high // Constants.access_width_bits) * (Constants.FIELD_HEIGHT + Constants.BORDER_WIDTH) - Constants.BORDER_WIDTH
