import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_with_tag_and_value(self):
        node = LeafNode(tag="p", value="This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")

    def test_to_html_without_tag_returns_raw_value(self):
        node = LeafNode(value="Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")

    def test_to_html_with_props(self):
        node = LeafNode(tag="a", value="Click me", props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://example.com" target="_blank">Click me</a>')

    def test_leaf_node_has_no_children(self):
        node = LeafNode(tag="p", value="Text")
        self.assertIsNone(node.children)


if __name__ == "__main__":
    unittest.main()
