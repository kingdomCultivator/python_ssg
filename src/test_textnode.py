import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("this is a text node", TextType.BOLD)
        node2 = TextNode("this is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("this is a different node", TextType.BOLD)
        self.assertNotEqual(node2, node3)

        node4 = TextNode("this is a different node", TextType.ITALIC)
        self.assertNotEqual(node4, node3)

        node5 = TextNode("this is a link node", TextType.LINK, "https://test.com")
        self.assertNotEqual(node4, node5)


if __name__ == "__main__":
    unittest.main()
