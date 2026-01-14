import re
from systemrdl.node import FieldNode

field_number = 0

def standard_scope(node):
    # return node.get_path_segment().lower()
    text = node.get_path_segment().lower() + "_" + node.__class__.__name__[0].lower()
    text = re.sub(r"(\d+)(?=[A-Za-z])", 'd', text)
    text = re.sub(r"_(?=\d)", "_d", text)
    text = re.sub(r"_+", "_", text)
    text = re.sub(r"^_+", "", text)
    if re.match(r"^[A-Za-z](?:\d|_)", text):
        text = "d" + text
    return text

def randomize_field(node: FieldNode):
    lines = []
    global field_number
    if node.is_hw_writable and node.is_hw_readable and node.is_sw_writable and node.is_sw_readable:
        field_size = node.high - node.low
        lines.append(f"   *hwif_in.{'.'.join(node.get_path_segments()[1:])}.next = $rand{field_number}{f'[{field_size}:0];' if field_size > 0 else ';'}")
        # if node.get_property("hwenable"):
        if node.is_hw_readable and node.is_hw_writable and node.get_property('hwenable'):
            lines.append(f"   *hwif_in.{'.'.join(node.get_path_segments()[1:])}.we = $rand{field_number+1};")
    field_number += 2
    return lines
