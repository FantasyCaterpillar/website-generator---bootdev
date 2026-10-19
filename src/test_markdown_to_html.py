import unittest
from markdown_to_html import *

class TestInline(unittest.TestCase):
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

    def test_quote(self):
        md = """
> This is a quote.
> This is a quote.
> This is a quote.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
                        '<div><blockquote>This is a quote. This is a quote. This is a quote.</blockquote></div>')

    def test_unordered_list(self):
        md = """
- Item 1
- Item 2
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
                        '<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>')

    def test_ordered_list(self):
        md = """
1. Item 1
2. Item 2
3. Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
                        '<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>')

    def test_mixed_markdown(self):
        md = """
## Shopping Notes

Buy **fresh** ingredients from the [market](https://example.com).

- Apples
- _Whole-grain_ bread

> Check the recipe first.

```
total = **not bold**
print(total)
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,'<div><h2>Shopping Notes</h2><p>Buy <b>fresh</b> ingredients from the <a href="https://example.com">market</a>.</p><ul><li>Apples</li><li><i>Whole-grain</i> bread</li></ul><blockquote>Check the recipe first.</blockquote><pre><code>total = **not bold**\nprint(total)\n</code></pre></div>')