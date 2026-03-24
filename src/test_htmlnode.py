# test_htmlnode.py

import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import text_node_to_html_node
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("p", "a paragraph.")
        node2 = HTMLNode("p", "a paragraph.")
        node3 = HTMLNode("p", "a paragraph.", None, {"href": "https://boot.dev"})
        node4 = HTMLNode("p", "a paragraph.", None, {"href": "https://boot.dev"})

        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)
        self.assertEqual(node3, node4)

        self.assertEqual(node3.props_to_html(), ' href="https://boot.dev"')


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node1 = LeafNode("p", "Hello, world!")
        self.assertEqual(node1.to_html(), "<p>Hello, world!</p>")
        node2 = LeafNode("h1", "HEY, world!")
        self.assertEqual(node2.to_html(), "<h1>HEY, world!</h1>")


class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node2 = ParentNode(
            "p",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        test_string_nested = "<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        test_string = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), test_string)
        self.assertEqual(node2.to_html(), test_string_nested)

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

    def test_text(self):
        node: TextNode = TextNode("This is a text node", TextType.TEXT)
        leaf_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, None)
        self.assertEqual(leaf_node.value, "This is a text node")
