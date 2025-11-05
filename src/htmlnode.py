



class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        # children should be assigned from the children parameter, not value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = []
        for key, value in self.props.items():
            props_html.append(f' {key}="{value}"')
        return "".join(props_html)

    def __repr__(self):
        return f"HTMLNode(\n TAG: {self.tag},\n VALUE: {self.value},\n CHILDREN: {self.children},\n PROPS: {self.props})"
    