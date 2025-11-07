from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERDED_LIST = 5
    ORDERED_LIST = 6
    HEADING2 = 7
    HEADING3 = 8
    HEADING4 = 9
    HEADING5 = 10
    HEADING6 = 11


def block_to_block_type(block_str):
    if block_str.startswith("#"):
        if block_str.startswith("##"):
            if block_str.startswith("###"):
                if block_str.startswith("####"):
                    if block_str.startswith("#####"):
                        if block_str.startswith("######"):
                            return BlockType.HEADING6
                        return BlockType.HEADING5
                    return BlockType.HEADING4
                return BlockType.HEADING3
            return BlockType.HEADING2
        return BlockType.HEADING
    elif block_str.startswith("`"):
        return BlockType.CODE
    elif block_str.startswith(">"):
        return BlockType.QUOTE
    elif block_str.startswith("- "):
        return BlockType.UNORDERDED_LIST
    elif block_str[0].isdigit() and ". " in block_str[:4]:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def block_type_to_html_tag(block_type):
    if block_type == BlockType.PARAGRAPH:
        return "p"
    elif block_type == BlockType.HEADING:
        return "h1"
    elif block_type == BlockType.HEADING2:
        return "h2"
    elif block_type == BlockType.HEADING3:
        return "h3"
    elif block_type == BlockType.HEADING4:
        return "h4"
    elif block_type == BlockType.HEADING5:
        return "h5"
    elif block_type == BlockType.HEADING6:
        return "h6"
    elif block_type == BlockType.CODE:
        return "pre"
    elif block_type == BlockType.QUOTE:
        return "blockquote"
    elif block_type == BlockType.UNORDERDED_LIST:
        return "ul"
    elif block_type == BlockType.ORDERED_LIST:
        return "ol"
    else:
        raise ValueError("Unsupported BlockType")
