from Constants import Constants

class Timeline:

    def __init__(self) -> None:
        return

    @property
    def slot_width(self) -> int:
        return Constants.access_width_bits * Constants.TIMELINE_SLOT_FIELD_WIDTH

    @property
    def width(self) -> int:
        return (self.slot_width + Constants.TIMELINE_SPACING) * Constants.number_of_time_slots - Constants.TIMELINE_SPACING

    @property
    def header_height(self) -> int:
        return Constants.TIMELINE_HEADER_HEIGHT
    
    @property
    def font_size(self) -> int:
        return 22
    
    @property
    def top(self) -> int:
        return -2 * Constants.TIMELINE_HEADER_HEIGHT
    
    @property
    def left(self) -> int:
        return Constants.access_width_bits * Constants.FIELD_WIDTH + (Constants.max_depth) * (Constants.NODE_WIDTH + Constants.SPACING) + Constants.REGISTER_NODE_WIDTH
    
    @property
    def spacing(self) -> int:
        return self.slot_width + Constants.TIMELINE_SPACING
