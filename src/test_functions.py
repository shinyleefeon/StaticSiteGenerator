import unittest

from functions import markdown_to_blocks, markdown_to_html_node, split_nodes_delimiter
from textnode import TextNode, TextType
from functions import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_bold_single_segment(self):
        nodes = [TextNode("This has **bold** text", TextType.PLAIN)]
        out = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(out), 3)
        self.assertEqual(out[0], TextNode("This has ", TextType.PLAIN))
        self.assertEqual(out[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(out[2], TextNode(" text", TextType.PLAIN))

    def test_split_italic_single_segment(self):
        nodes = [TextNode("An *italic* word", TextType.PLAIN)]
        out = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertEqual(out, [
            TextNode("An ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.PLAIN),
        ])

    def test_split_code_single_segment(self):
        nodes = [TextNode("Use `code` here", TextType.PLAIN)]
        out = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(out, [
            TextNode("Use ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.PLAIN),
        ])

    def test_raises_on_unbalanced_delimiters(self):
        nodes = [TextNode("This is **broken", TextType.PLAIN)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

    def test_pass_through_non_plain_and_no_delimiter_plain(self):
        # Non-plain nodes should pass through untouched
        bold_node = TextNode("already bold", TextType.BOLD)
        # Plain node without delimiters should remain as-is
        plain_node = TextNode("no markers here", TextType.PLAIN)
        out = split_nodes_delimiter([bold_node, plain_node], "**", TextType.BOLD)
        self.assertEqual(out[0], bold_node)
        self.assertEqual(out[1], plain_node)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_image_single(self):
        node = TextNode(
            "Text with ![alt text](https://example.com/image.png) here",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("Text with ", TextType.PLAIN))
        self.assertEqual(new_nodes[1], TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"))
        self.assertEqual(new_nodes[2], TextNode(" here", TextType.PLAIN))

    def test_split_nodes_image_no_image(self):
        node = TextNode("Just plain text without images", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_split_nodes_link_single(self):
        node = TextNode(
            "Check out [this link](https://www.example.com) for more info",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("Check out ", TextType.PLAIN))
        self.assertEqual(new_nodes[1], TextNode("this link", TextType.LINK, "https://www.example.com"))
        self.assertEqual(new_nodes[2], TextNode(" for more info", TextType.PLAIN))

    def test_split_nodes_link_no_link(self):
        node = TextNode("Just plain text without links", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_plain_only(self):
        text = "This is just plain text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0], TextNode("This is just plain text", TextType.PLAIN))

    def test_text_to_textnodes_bold_only(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0], TextNode("This is ", TextType.PLAIN))
        self.assertEqual(nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(nodes[2], TextNode(" text", TextType.PLAIN))

    def test_text_to_textnodes_italic_only(self):
        text = "__italic__"
        nodes = text_to_textnodes(text)
        expected = [TextNode("italic", TextType.ITALIC)]

    def test_text_to_textnodes_code_only(self):
        text = "This is `code` text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0], TextNode("This is ", TextType.PLAIN))
        self.assertEqual(nodes[1], TextNode("code", TextType.CODE))
        self.assertEqual(nodes[2], TextNode(" text", TextType.PLAIN))

    def test_text_to_textnodes_all_types_mixed(self):
        text = "This is **bold** and _italic_ and `code` and ![image](https://example.com/img.png) and [link](https://example.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(len(nodes), len(expected))
        for i, node in enumerate(nodes):
            self.assertEqual(node, expected[i])

    def test_text_to_textnodes_multiple_same_type(self):
        text = "**bold1** some text **bold2** more text **bold3**"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes[0], TextNode("bold1", TextType.BOLD))
        self.assertEqual(nodes[1], TextNode(" some text ", TextType.PLAIN))
        self.assertEqual(nodes[2], TextNode("bold2", TextType.BOLD))
        self.assertEqual(nodes[3], TextNode(" more text ", TextType.PLAIN))
        self.assertEqual(nodes[4], TextNode("bold3", TextType.BOLD))

    def test_text_to_textnodes_multiple_images_and_links(self):
        text = "![img1](url1) text [link1](url2) more ![img2](url3) text [link2](url4)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes[0], TextNode("img1", TextType.IMAGE, "url1"))
        self.assertEqual(nodes[1], TextNode(" text ", TextType.PLAIN))
        self.assertEqual(nodes[2], TextNode("link1", TextType.LINK, "url2"))
        self.assertEqual(nodes[3], TextNode(" more ", TextType.PLAIN))
        self.assertEqual(nodes[4], TextNode("img2", TextType.IMAGE, "url3"))
        self.assertEqual(nodes[5], TextNode(" text ", TextType.PLAIN))
        self.assertEqual(nodes[6], TextNode("link2", TextType.LINK, "url4"))

    def test_text_to_textnodes_all_types_with_multiple_bold(self):
        text = "This is **bold1** and _italic_ with `code` and **bold2** plus ![image](img.png) and **bold3** and [link](url)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.PLAIN),
            TextNode("bold2", TextType.BOLD),
            TextNode(" plus ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "img.png"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("bold3", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "url"),
        ]
        self.assertEqual(len(nodes), len(expected))
        for i, node in enumerate(nodes):
            self.assertEqual(node, expected[i])

        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )



    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )


class TestMarkdownToHTMLNodeEdgeCases(unittest.TestCase):
    def test_empty_markdown(self):
        """Test that empty markdown string produces empty div"""
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_unordered_list_with_inline_formatting(self):
        """Test unordered list items maintain inline formatting"""
        md = """
- First item
- Second item with **bold**
- Third item with _italic_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item with <b>bold</b></li><li>Third item with <i>italic</i></li></ul></div>",
        )

    def test_ordered_list_single_item(self):
        """Test ordered list with a single item (double digit)"""
        md = """
10. Only one item here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Only one item here</li></ol></div>",
        )

    def test_quote_with_inline_formatting(self):
        """Test quote block with bold and italic formatting"""
        md = """
> This is a **bold** quote with _italic_ text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a <b>bold</b> quote with <i>italic</i> text</blockquote></div>",
        )
    
    def test_mixed_blocks_complex(self):
        """Test complex markdown with multiple block types mixed together"""
        md = """
# Header

This is a paragraph with **bold** and `code`.

> A quote here

- List item one
- List item two
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Header</h1><p>This is a paragraph with <b>bold</b> and <code>code</code>.</p><blockquote>A quote here</blockquote><ul><li>List item one</li><li>List item two</li></ul></div>",
        )

    


if __name__ == "__main__":
    unittest.main()