import unittest

from blocks import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "# Heading 1"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_code_block(self):
        block = "```python\nprint('hello')\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_quote(self):
        block = "> This is a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- Item 1"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERDED_LIST)


if __name__ == "__main__":
    unittest.main()
