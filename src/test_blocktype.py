import unittest
from blocktype import *

class TestBlockType(unittest.TestCase):

    def test_block_to_blocktype_heading(self):
        md = '# Heading 1'
        blocks = block_to_block_type(md)
        self.assertEqual(
            blocks,
            BlockType.heading
        )

    def test_block_to_blocktype_code(self):
        md = """```
This is code
```"""
        blocks = block_to_block_type(md)
        self.assertEqual(
            blocks,
            BlockType.code
        )

    def test_block_to_blocktype_quote(self):
        md = "> This is a quote."
        blocks = block_to_block_type(md)
        self.assertEqual(
            blocks,
            BlockType.quote
        )   

    def test_block_to_blocktype_unordered_list(self):
        md = """- Item 1
- Item 2
- Item 3"""
        blocks = block_to_block_type(md)
        self.assertEqual(
            blocks,
            BlockType.unordered_list
        )   

    def test_block_to_blocktype_ordered_list(self):
        md = """1. Item 1
2. Item 2
3. Item 3"""
        blocks = block_to_block_type(md)
        self.assertEqual(
            blocks,
            BlockType.ordered_list
        )

    def test_block_to_blocktype_paragraph(self):
        md = 'normal paragraph'
        blocks = block_to_block_type(md)
        self.assertEqual(
            blocks,
            BlockType.paragraph
        )