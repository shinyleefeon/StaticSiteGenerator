from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)
        self.tag = tag
        self.value = value
        self.props = props
        self.children = None  # Leaf nodes do not have children

    def to_html(self):
        # Handle self-closing tags (like img) that don't need a value
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()} />"
        
        if self.value is None:
            raise ValueError("LeafNode must have a value to convert to HTML")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
