import math

class Size:

    SIZES = {
        "FIELD_WIDTH": {1:50, 2:50, 4:50, 8:50},
        "FIELD_HEIGHT": {1:70, 2:110, 4:130, 8:150},
        "REGISTER_NODE_WIDTH": {1:90, 2:180, 4:350, 8:90},
        "NODE_WIDTH": {1:50, 2:75, 4:100, 8:50},
        "SPACING": {1:25, 2:45, 4:60, 8:25},
        "BORDER_WIDTH": {1:10, 2:10, 4:10, 8:10},
        "NODE_FONT_SIZE": {1:12, 2:22, 4:30, 8:12},
        "REGISTER_FONT_SIZE": {1:12, 2:18, 4:25, 8:12},
        "FIELD_LABEL_FONT_SIZE": {1:[8, 12, 12], 2:[8, 16, 16], 4:[10, 20, 20], 8:[8, 12, 12]},
        "FIELD_VALUE_FONT_SIZE": {1:[22, 20, 20], 2:[32, 30, 30], 4:[46, 32, 44], 8:[22, 20, 20]},
        "TIMELINE_SLOT_FIELD_WIDTH": {1:15, 2:15, 4:15, 8:15},
        "TIMELINE_SLOT_FIELD_HEIGHT": {1:30, 2:50, 4:60, 8:70},
        "TIMELINE_SPACING": {1:50, 2:40, 4:40, 8:40},
        "TIMELINE_HEADER_HEIGHT": {1:40, 2:40, 4:40, 8:40},
    }


    def __init__(self, access_width):

        self.access_width_bits = access_width
        self.access_width_bytes = math.ceil(access_width // 8)
        self.field_width = self.SIZES["FIELD_WIDTH"][self.access_width_bytes]
        self.field_height = self.SIZES["FIELD_HEIGHT"][self.access_width_bytes]
        self.register_node_width = self.SIZES["REGISTER_NODE_WIDTH"][self.access_width_bytes]
        self.node_width = self.SIZES["NODE_WIDTH"][self.access_width_bytes]
        self.spacing = self.SIZES["SPACING"][self.access_width_bytes]
        self.border_width = self.SIZES["BORDER_WIDTH"][self.access_width_bytes]
        self.node_font_size = self.SIZES["NODE_FONT_SIZE"][self.access_width_bytes]
        self.register_font_size = self.SIZES["REGISTER_FONT_SIZE"][self.access_width_bytes]
        self.field_label_font_size = self.SIZES["FIELD_LABEL_FONT_SIZE"][self.access_width_bytes]
        self.field_value_font_size = self.SIZES["FIELD_VALUE_FONT_SIZE"][self.access_width_bytes]
        self.timeline_slot_field_width = self.SIZES["TIMELINE_SLOT_FIELD_WIDTH"][self.access_width_bytes]
        self.timeline_slot_field_height = self.SIZES["TIMELINE_SLOT_FIELD_HEIGHT"][self.access_width_bytes]
        self.timeline_spacing = self.SIZES["TIMELINE_SPACING"][self.access_width_bytes]
        self.timeline_header_height = self.SIZES["TIMELINE_HEADER_HEIGHT"][self.access_width_bytes]

        self.timeline_slot_width = self.access_width_bits * self.timeline_slot_field_width

    def get_no_of_words(self, size):
        return math.ceil(size / self.access_width_bytes)

    def get_node_height(self, size):
        return self.get_no_of_words(size) * (self.field_height + self.border_width) - 3 * self.border_width
    
    @property
    def space_view_left(self) -> int:
        pass

    @property
    def timeline_left(self) -> int:
        return self.access_width_bits * self.field_width + self.register_node_width + self.node_width + self.spacing
    
    @property
    def timeline_slot_height(self) -> int:
        return self.field_height - 20