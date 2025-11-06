import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_neq_different_text(self):
        node = TextNode("a", TextType.PLAIN)
        node2 = TextNode("b", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_default_text_type_is_plain(self):
        node = TextNode("plain text")
        self.assertEqual(node.text_type, TextType.PLAIN)

    def test_repr_includes_value_and_url(self):
        node = TextNode("link", TextType.LINK, url="http://example.com")
        expected = f"TextNode({node.text}, {node.text_type.value}, {node.url})"
        self.assertEqual(repr(node), expected)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_node_to_html_node_link(self):
        node = TextNode("Click here", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_text_node_to_html_node_image(self):
        node = TextNode("Alt text", TextType.IMAGE, url="https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "Alt text"})


if __name__ == "__main__":
    unittest.main()