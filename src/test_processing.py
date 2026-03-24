# test_processing.py

import unittest

from markdown_to_blocks import BlockType, block_to_block_type, markdown_to_blocks
from textnode import (
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestSplitDelimiters(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode(
            "This is the **end** of everything, we'll lose our _divisions_ and forget our names",
            TextType.TEXT,
        )
        # case1 = [
        #     TextNode("This is the ", TextType.TEXT),
        #     TextNode("end", TextType.BOLD),
        #     TextNode(
        #         " of everything, we'll lose our _divisions_ and forget our names",
        #         TextType.TEXT,
        #     ),
        # ]
        case2 = [
            TextNode("This is the ", TextType.TEXT),
            TextNode("end", TextType.BOLD),
            TextNode(" of everything, we'll lose our ", TextType.TEXT),
            TextNode("divisions", TextType.ITALIC),
            TextNode(" and forget our names", TextType.TEXT),
        ]

        unbold = split_nodes_delimiter([node1], "**", TextType.BOLD)
        # print(f"\n{unbold}: unbold\n")
        # print(f"\n{case1}: case1\n")
        unitalic = split_nodes_delimiter(
            unbold,
            "_",
            TextType.ITALIC,
        )
        # print(f"\n{unitalic}: unitalic\n")
        # print(f"\n{case2}: case2\n")
        self.assertEqual(
            unitalic,
            case2,
        )
        test_text = "Super duper easy image link test ![alt-text](https://boot.dev)"
        test_text_comp = [("alt-text", "https://boot.dev")]
        self.assertEqual(extract_markdown_images(test_text), test_text_comp)

        test_text1 = "Super duper easy image link test ![alt-text](https://boot.dev) and this one too ![boobywooby-text](https://boot.devagain)"
        test_text_comp1 = [
            ("alt-text", "https://boot.dev"),
            ("boobywooby-text", "https://boot.devagain"),
        ]
        self.assertEqual(extract_markdown_images(test_text1), test_text_comp1)

        test_text2 = "Super duper easy image link test [alt-text](https://boot.dev)"
        test_text_comp2 = [("alt-text", "https://boot.dev")]
        self.assertEqual(extract_markdown_links(test_text2), test_text_comp2)

        test_text3 = "Super duper easy image link test [alt-text](https://boot.dev) and this one too ![boobywooby-text](https://boot.devagain)"
        test_text_comp3 = [
            ("alt-text", "https://boot.dev"),
        ]
        self.assertEqual(extract_markdown_links(test_text3), test_text_comp3)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_text_to_nodes(self):
        test_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        case_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertListEqual(text_to_textnodes(test_text), case_nodes)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

1. This is an ordered list
2. This is a second entry

```Here is some code```

> this is a quote
> so is this

# This is a heading
## This is not a heading
### This is not another another heading


## this is another heading
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                "1. This is an ordered list\n2. This is a second entry",
                "```Here is some code```",
                "> this is a quote\n> so is this",
                "# This is a heading\n## This is not a heading\n### This is not another another heading",
                "## this is another heading",
            ],
        )

        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(blocks[0]))
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(blocks[2]))
        self.assertEqual(BlockType.CODE, block_to_block_type(blocks[4]))
        self.assertEqual(BlockType.HEADING, block_to_block_type(blocks[6]))
        self.assertEqual(BlockType.HEADING, block_to_block_type(blocks[7]))
        self.assertEqual(BlockType.QUOTE, block_to_block_type(blocks[5]))
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(blocks[3]))


if __name__ == "__main__":
    unittest.main()
