import unittest
from htmlnode import HTMLNode,LeafNode,ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_not_eq_tag(self):
        node = HTMLNode('p','lorem ipsum')
        node2 = HTMLNode('y','lorem ipsum')
        self.assertNotEqual(node, node2)

    def test_not_eq_value(self):
        node = HTMLNode('y','lorem')
        node2 = HTMLNode('y','lorem ipsum')
        self.assertNotEqual(node, node2)

    def test_not_eq_children(self):
        node = HTMLNode('y','lorem ipsum', ['ugo','fiero'])
        node2 = HTMLNode('y','lorem ipsum', ['ugo','nano'])
        self.assertNotEqual(node, node2)
        
    def test_not_eq_attribute(self):
        attributes = {
        "href": "https://www.google.com",
        "target": "_blank",
    }
        node = HTMLNode('y','lorem ipsum',['ugo','fiero'], attributes)
        node2 = HTMLNode('y','lorem ipsum',['ugo','fiero'])
        self.assertNotEqual(node, node2)

    def test_eq_html_conversion(self):
        attributes = {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        node = HTMLNode('y','lorem ipsum',['ugo','fiero'], attributes)
        html_node = node.props_to_html()
        expected_node = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(html_node,expected_node)

    def test_eq_repr(self):
        attributes = {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        node = HTMLNode('y','lorem ipsum',['ugo','fiero'], attributes)
        print(node)

    ## Leaf Node tests
    # basic functions

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    # Tags tests
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(),'<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(),'<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Heading 1", {})
        self.assertEqual(node.to_html(),'<h1>Heading 1</h1>')

    ## we check if the value errors works correctly
    def test_leaf_to_html_no_value(self):
        node = LeafNode("a", "", {"href": "https://www.google.com"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_no_tag(self):
        node = LeafNode("", "grodo", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(),'grodo')

    ## Parent Node Tests

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

    def test_to_html_with_childrens(self):
        child_node1 = LeafNode("span", "child")
        child_node2 = LeafNode("ram", "child")
        parent_node = ParentNode("div", [child_node1,child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><ram>child</ram></div>")


    def test_to_html_without_children(self):
        parent_node = ParentNode("div",[])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_without_tag(self):
            child_node1 = LeafNode("span", "child")
            child_node2 = LeafNode("ram", "child")
            parent_node = ParentNode("",[child_node1,child_node2])
            with self.assertRaises(ValueError):
                parent_node.to_html()