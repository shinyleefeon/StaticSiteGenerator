import unittest

from textnode import TextNode, TextType

import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()