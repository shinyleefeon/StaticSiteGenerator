import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_single_child(self):
        child = LeafNode(tag="span", value="Hello")
        parent = ParentNode(tag="div", children=[child])
        self.assertEqual(parent.to_html(), "<div><span>Hello</span></div>")

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode(tag="b", value="Bold")
        child2 = LeafNode(tag="i", value="Italic")
        child3 = LeafNode(value="Plain")
        parent = ParentNode(tag="p", children=[child1, child2, child3])
        self.assertEqual(parent.to_html(), "<p><b>Bold</b><i>Italic</i>Plain</p>")

    def test_to_html_raises_error_without_tag(self):
        child = LeafNode(tag="span", value="Hello")
        parent = ParentNode(tag=None, children=[child])
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertIn("must have a tag", str(context.exception))

    def test_to_html_raises_error_without_children(self):
        parent = ParentNode(tag="div", children=None)
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertIn("must have children", str(context.exception))

    def test_to_html_with_props(self):
        child = LeafNode(tag="span", value="Content")
        parent = ParentNode(tag="div", children=[child], props={"class": "container", "id": "main"})
        self.assertEqual(parent.to_html(), '<div class="container" id="main"><span>Content</span></div>')

    def test_to_html_with_nested_parents(self):
        leaf1 = LeafNode(tag="b", value="Bold text")
        leaf2 = LeafNode(value="Normal text")
        inner_parent = ParentNode(tag="span", children=[leaf1, leaf2])
        outer_parent = ParentNode(tag="div", children=[inner_parent])
        self.assertEqual(outer_parent.to_html(), "<div><span><b>Bold text</b>Normal text</span></div>")

    def test_to_html_with_many_nested_children(self):
        leaf1 = LeafNode(tag="li", value="Item 1")
        leaf2 = LeafNode(tag="li", value="Item 2")
        leaf3 = LeafNode(tag="li", value="Item 3")
        ul = ParentNode(tag="ul", children=[leaf1, leaf2, leaf3])
        self.assertEqual(ul.to_html(), "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
