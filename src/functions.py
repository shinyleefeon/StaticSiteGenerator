import re
import os
import shutil

from parentnode import ParentNode
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
    final_nodes = split_nodes_delimiter(final_nodes, "_", TextType.ITALIC)
    final_nodes = split_nodes_delimiter(final_nodes, "`", TextType.CODE)
    final_nodes = split_nodes_image(final_nodes)
    final_nodes = split_nodes_link(final_nodes)

    return final_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    formatted = []
    for block in blocks:
        if block.strip() == "":
            continue
        newblock = block.strip()
        formatted.append(newblock)
    return formatted



def markdown_to_html_node(markdown):
    from htmlnode import HTMLNode
    from leafnode import LeafNode
    from textnode import TextNode, TextType
    from blocks import block_to_block_type, block_type_to_html_tag, BlockType
    
    blocks = markdown_to_blocks(markdown)
    root = ParentNode(tag="div", children=[])
    for block in blocks:
        type = block_to_block_type(block)
        node =  ParentNode(tag=block_type_to_html_tag(type), children=[])
        if type == BlockType.PARAGRAPH:
            # Replace newlines with spaces for paragraphs
            node.value = " ".join(block.split())
        elif type == BlockType.HEADING:
            node.value = block.lstrip("# ").strip()
        elif type == BlockType.HEADING2:
            node.value = block.lstrip("# ").strip()
        elif type == BlockType.HEADING3:
            node.value = block.lstrip("# ").strip()
        elif type == BlockType.HEADING4:
            node.value = block.lstrip("# ").strip()
        elif type == BlockType.HEADING5:
            node.value = block.lstrip("# ").strip()
        elif type == BlockType.HEADING6:
            node.value = block.lstrip("# ").strip()
        elif type == BlockType.CODE:
            node.value = block.strip("`").strip()
        elif type == BlockType.QUOTE:
            node.value = block.lstrip("> ").strip()
        elif type == BlockType.UNORDERDED_LIST:
            items = block.lstrip("- ").split("\n- ")
            for item in items:
                item_node = ParentNode(tag="li", children=[])
                text_nodes = text_to_textnodes(item.strip())
                for text_node in text_nodes:
                    html_leaf = text_node_to_html_node(text_node)
                    item_node.children.append(html_leaf)
                node.children.append(item_node)
        elif type == BlockType.ORDERED_LIST:
            items = re.split(r"\d+\. ", block)[1:]  # Skip the first empty split
            for item in items:
                item_node = ParentNode(tag="li", children=[])
                text_nodes = text_to_textnodes(item.strip())
                for text_node in text_nodes:
                    html_leaf = text_node_to_html_node(text_node)
                    item_node.children.append(html_leaf)
                node.children.append(item_node)
        else:
            raise ValueError("Unsupported BlockType")
        
        # Apply inline formatting to paragraphs, headings, and quotes
        if type in (BlockType.PARAGRAPH, BlockType.HEADING, BlockType.HEADING2, BlockType.HEADING3, 
                    BlockType.HEADING4, BlockType.HEADING5, BlockType.HEADING6, BlockType.QUOTE):
            text_nodes = text_to_textnodes(node.value)
            for text_node in text_nodes:
                html_leaf = text_node_to_html_node(text_node)
                node.children.append(html_leaf)
            node.value = None
        elif type == BlockType.CODE:
            node.children = []
            text_node = TextNode(text=node.value, text_type=TextType.CODE)
            node.children.append(text_node_to_html_node(text_node))
            node.value = None

        root.children.append(node)
    return root
    

def recursive_copy(src, dest):
    """Recursively copy contents of directory `src` into directory `dest`.

    Behavior:
    - If `dest` exists, it will be removed and recreated (top-level only).
    - Copies files with metadata (shutil.copy2).
    - Recursively copies subdirectories.
    """

    if not os.path.isdir(src):
        raise ValueError("Source must be a directory")

    # Clean destination directory only at the top level
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest, exist_ok=True)

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            # Recursively copy subdirectory
            os.makedirs(d, exist_ok=True)
            for sub in os.listdir(s):
                sub_src = os.path.join(s, sub)
                sub_dest = os.path.join(d, sub)
                if os.path.isdir(sub_src):
                    recursive_copy(sub_src, sub_dest)
                else:
                    shutil.copy2(sub_src, sub_dest)
        else:
            # Copy regular file
            shutil.copy2(s, d)

def extract_title(markdown):
    """Extract the title from markdown content.

    The title is defined as the first level-1 heading (starting with '# ').
    If no level-1 heading is found, return 'Untitled'.
    """
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No level-1 heading found for title extraction")


def generate_page(from_path, template_path, dest_path, basepath="/"):
    #Generate an HTML page from markdown content using a template.

    print(f"Generating page from {from_path} to {dest_path}")
    markdown = open(from_path, "r", encoding="utf-8").read()
    template = open(template_path, "r", encoding="utf-8").read()
    title = extract_title(markdown)
    html_node = markdown_to_html_node(markdown)
    content_html = ""
    for child in html_node.children:
        content_html += child.to_html()
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
    final_html = final_html.replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")
    os.makedirs(dest_path, exist_ok=True)
    output_file = os.path.join(dest_path, "index.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_html) 


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    directory = os.listdir(dir_path_content)
    for item in directory:
        src_path = os.path.join(dir_path_content, item)
        if os.path.isdir(src_path):
            # If it's a directory, recurse with the same logic
            dest_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(src_path, template_path, dest_path, basepath)
        elif item.endswith(".md"):
            # If it's a markdown file, generate the page
            if item == "index.md":
                # Special case for index.md, output to the parent directory
                dest_path = dest_dir_path
            else:
                # For other .md files, create a subdirectory
                dest_path = os.path.join(dest_dir_path, item.replace(".md", ""))
            generate_page(src_path, template_path, dest_path, basepath)