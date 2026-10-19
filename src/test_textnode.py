import unittest
from textnode import TextNode, TextType,text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_if_url_none(self):
        node = TextNode("This is a text node", TextType.LINK, None)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node, node2)

    def test_not_eq_texttype(self):
        #different texttype
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_text(self):
        #different text
        node3 = TextNode("This is a text", TextType.BOLD)
        node4 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node3, node4)

    def test_not_eq_url(self):
        #different url
        node5 = TextNode("This is a text node", TextType.LINK,'grodo')
        node6 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node5, node6)

    ## test HTML conversion
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode('this is a link node', TextType.LINK,'www.mauro.net')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props, {'href': 'www.mauro.net'})
        self.assertEqual(html_node.value, 'this is a link node')
        self.assertEqual(html_node.tag, 'a')

    def test_image(self):
        node = TextNode("this is a image node", TextType.IMAGE, 'www.maurob.net')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props, {'alt': 'this is a image node','src': 'www.maurob.net'})
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.tag, 'img')

    def test_text_type_error(self):
        node = TextNode("This is a text node", 'gogo')
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()