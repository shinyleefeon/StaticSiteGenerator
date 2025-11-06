from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, props=props, children=children)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag to convert to HTML")
        if self.children is None:
            raise ValueError("ParentNode must have children to convert to HTML")
        final_html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            final_html += child.to_html()
        final_html += f"</{self.tag}>"
        return final_html
        
