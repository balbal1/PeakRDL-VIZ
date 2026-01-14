from systemrdl.node import AddrmapNode, MemNode
from systemrdl.node import RegNode, RegfileNode, FieldNode

class Constants:

    access_width_bits = 32
    access_width_bytes = 4
    base_address = 0
    max_depth = 1
    number_of_time_slots = 51

    constants = {
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

    COLOR_CODES = {
        AddrmapNode: "D0E4EE",
        MemNode: "D5D1E9",
        RegfileNode: "F5CF9F",
        RegNode: "F5A7A6",
        FieldNode: "F3F5A9",
        "BLANK": "AAAAAA"
    }

    @staticmethod
    def set_constants():
        Constants.FIELD_WIDTH = Constants.constants["FIELD_WIDTH"][Constants.access_width_bytes]
        Constants.FIELD_HEIGHT = Constants.constants["FIELD_HEIGHT"][Constants.access_width_bytes]
        Constants.REGISTER_NODE_WIDTH = Constants.constants["REGISTER_NODE_WIDTH"][Constants.access_width_bytes]
        Constants.NODE_WIDTH = Constants.constants["NODE_WIDTH"][Constants.access_width_bytes]
        Constants.SPACING = Constants.constants["SPACING"][Constants.access_width_bytes]
        Constants.BORDER_WIDTH = Constants.constants["BORDER_WIDTH"][Constants.access_width_bytes]
        Constants.NODE_FONT_SIZE = Constants.constants["NODE_FONT_SIZE"][Constants.access_width_bytes]
        Constants.REGISTER_FONT_SIZE = Constants.constants["REGISTER_FONT_SIZE"][Constants.access_width_bytes]
        Constants.FIELD_LABEL_FONT_SIZE = Constants.constants["FIELD_LABEL_FONT_SIZE"][Constants.access_width_bytes]
        Constants.FIELD_VALUE_FONT_SIZE = Constants.constants["FIELD_VALUE_FONT_SIZE"][Constants.access_width_bytes]
        Constants.TIMELINE_SLOT_FIELD_WIDTH = Constants.constants["TIMELINE_SLOT_FIELD_WIDTH"][Constants.access_width_bytes]
        Constants.TIMELINE_SLOT_FIELD_HEIGHT = Constants.constants["TIMELINE_SLOT_FIELD_HEIGHT"][Constants.access_width_bytes]
        Constants.TIMELINE_SPACING = Constants.constants["TIMELINE_SPACING"][Constants.access_width_bytes]
        Constants.TIMELINE_HEADER_HEIGHT = Constants.constants["TIMELINE_HEADER_HEIGHT"][Constants.access_width_bytes]

        Constants.WORD_WIDTH = Constants.access_width_bits * Constants.FIELD_WIDTH + Constants.BORDER_WIDTH
        Constants.WORD_HEIGHT = Constants.FIELD_HEIGHT + Constants.BORDER_WIDTH
        Constants.TIMELINE_SLOT_WIDTH = Constants.access_width_bits * Constants.TIMELINE_SLOT_FIELD_WIDTH
        Constants.TIMELINE_LEFT = Constants.access_width_bits * Constants.FIELD_WIDTH + Constants.REGISTER_NODE_WIDTH + Constants.NODE_WIDTH + Constants.SPACING
        Constants.TIMELINE_SLOT_HEIGHT = Constants.FIELD_HEIGHT - 20

    @staticmethod
    def set_access_width(access_width):
        Constants.access_width_bits = access_width
        Constants.access_width_bytes = access_width // 8 if access_width % 8 == 0 else access_width // 8 + 1

    @staticmethod
    def set_base_address(base_address):
        Constants.base_address = base_address

    @staticmethod
    def set_max_depth(max_depth):
        Constants.max_depth = max_depth
