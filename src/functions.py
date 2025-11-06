import re

from textnode import text_node_to_html_node



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    from textnode import TextNode, TextType

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        # No delimiter -> keep node as-is
        if len(parts) == 1:
            new_nodes.append(node)
            continue
        
        # Must be balanced (odd number of parts)
        if len(parts) % 2 == 0:
            raise ValueError("Invalid number of delimiters in text node")

        for i, segment in enumerate(parts):
            if segment == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(segment, TextType.PLAIN))
            else:
                new_nodes.append(TextNode(segment, text_type))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    from textnode import TextNode, TextType

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        extracted = extract_markdown_images(text=node.text)
        if not extracted:
            new_nodes.append(node)
            continue
        
        # Process first image
        image_alt = extracted[0][0]
        image_link = extracted[0][1]
        sections = node.text.split(f"![{image_alt}]({image_link})", 1)
        
        # Add text before image
        if sections[0]:
            new_nodes.append(TextNode(sections[0], TextType.PLAIN))
        
        # Add image node
        new_nodes.append(TextNode(image_alt, TextType.IMAGE, url=image_link))
        
        # Recursively process remaining text for more images
        if len(sections) > 1 and sections[1]:
            remaining_nodes = split_nodes_image([TextNode(sections[1], TextType.PLAIN)])
            new_nodes.extend(remaining_nodes)
            
    return new_nodes

def split_nodes_link(old_nodes):
    from textnode import TextNode, TextType

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        extracted = extract_markdown_links(text=node.text)
        if not extracted:
            new_nodes.append(node)
            continue
        
        # Process first link
        link_text = extracted[0][0]
        link_url = extracted[0][1]
        sections = node.text.split(f"[{link_text}]({link_url})", 1)
        
        # Add text before link
        if sections[0]:
            new_nodes.append(TextNode(sections[0], TextType.PLAIN))
        
        # Add link node
        new_nodes.append(TextNode(link_text, TextType.LINK, url=link_url))
        
        # Recursively process remaining text for more links
        if len(sections) > 1 and sections[1]:
            remaining_nodes = split_nodes_link([TextNode(sections[1], TextType.PLAIN)])
            new_nodes.extend(remaining_nodes)
            
    return new_nodes

def text_to_textnodes(text):
    from textnode import TextNode, TextType
    final_nodes = []

    final_nodes = split_nodes_delimiter([TextNode(text, TextType.PLAIN)], "**", TextType.BOLD)
    final_nodes = split_nodes_delimiter(final_nodes, "__", TextType.ITALIC)
    final_nodes = split_nodes_delimiter(final_nodes, "`", TextType.CODE)
    final_nodes = split_nodes_image(final_nodes)
    final_nodes = split_nodes_link(final_nodes)

    return final_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    formatted = []
    for block in blocks:
        if block == "":
            blocks.remove(block)
        newblock = block.strip()
        formatted.append(newblock)
    return formatted



def markdown_to_html_node(markdown):
    from htmlnode import HTMLNode
    from leafnode import LeafNode
    from textnode import TextNode, TextType
    from blocks import block_to_block_type, block_type_to_html_tag, BlockType
    
    blocks = markdown_to_blocks(markdown)
    root = HTMLNode(tag="div", children=[])
    for block in blocks:
        type = block_to_block_type(block)
        node =  LeafNode(tag=block_type_to_html_tag(type))
        if type == BlockType.PARAGRAPH:
            node.value = block
        elif type == BlockType.HEADING:
            node.value = block.lstrip("# ").strip()
        elif type == BlockType.CODE:
            node.value = block.strip("`").strip()
        elif type == BlockType.QUOTE:
            node.value = block.lstrip("> ").strip()
        elif type == BlockType.UNORDERDED_LIST:
            items = block.lstrip("- ").split("\n- ")
            for item in items:
                item_node = HTMLNode(tag="li", value=item.strip())
                node.children.append(item_node)
        elif type == BlockType.ORDERED_LIST:
            items = re.split(r"\d+\. ", block)[1:]  # Skip the first empty split
            for item in items:
                item_node = HTMLNode(tag="li", value=item.strip())
                node.children.append(item_node)
        else:
            raise ValueError("Unsupported BlockType")
        if type != BlockType.CODE:
            text_nodes = text_to_textnodes(node.value)
            node.children = []
            for text_node in text_nodes:
                html_leaf = text_node_to_html_node(text_node)
                node.children.append(html_leaf)
            node.value = None
        else:
            node.children = []
            text_node = TextNode(text=node.value, text_type=TextType.CODE)
            node.children.append(text_node_to_html_node(text_node))
            node.value = None

        root.children.append(node)

