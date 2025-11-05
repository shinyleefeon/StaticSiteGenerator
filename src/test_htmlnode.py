import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
	def test_props_to_html_returns_string(self):
		node = HTMLNode(tag="a", props={"href": "https://example.com", "target": "_blank"})
		result = node.props_to_html()
		self.assertEqual(result, ' href="https://example.com" target="_blank"')

	def test_children_are_assigned(self):
		child1 = HTMLNode(tag="span", value="Hello")
		child2 = HTMLNode(tag="strong", value="World")
		parent = HTMLNode(tag="p", children=[child1, child2])
		self.assertEqual(parent.children, [child1, child2])

	def test_to_html_not_implemented(self):
		node = HTMLNode(tag="div", value="content")
		with self.assertRaises(NotImplementedError):
			node.to_html()


if __name__ == "__main__":
	unittest.main()
