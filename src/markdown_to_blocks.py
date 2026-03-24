# markdown_to_blocks()


import string
from enum import Enum

from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node, text_to_children


class BlockType(Enum):
    PARAGRAPH = ("PARAGRAPH",)
    HEADING = ("HEADING",)
    CODE = ("CODE",)
    QUOTE = ("QUOTE",)
    UNORDERED_LIST = ("UNORDERED_LIST",)
    ORDERED_LIST = ("ORDERED_LIST",)


def markdown_to_blocks(markdown: str) -> list[str]:
    block_list = markdown.split("\n\n")
    out_list = []
    for b in block_list:
        cb = b.strip()
        if len(cb) > 0:
            out_list.append(cb)
    return out_list


def block_to_block_type(block: str) -> BlockType:
    if block[0] == "#":
        count = 1
        for c in block[1:]:
            if count < 7:
                if c == "#":
                    count += 1
                elif c == " ":
                    return BlockType.HEADING
        else:
            return BlockType.PARAGRAPH
    elif block[0:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    elif block[0] == ">":
        return BlockType.QUOTE
    elif block[0:2] == "- ":
        return BlockType.UNORDERED_LIST
    elif block[0] in string.digits and block[1:3] == ". ":
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def block_to_html_node(block: str) -> HTMLNode:
    btype: BlockType = block_to_block_type(block)
    match btype:
        case BlockType.PARAGRAPH:
            block = block.replace("\n", " ")
            children: list = text_to_children(block)
            return ParentNode("p", children, None)
        case BlockType.HEADING:
            h_count = 0
            for c in block:
                if c != "#":
                    break
                else:
                    h_count += 1
            heading_text = block.lstrip("# ")
            return LeafNode(f"h{h_count}", heading_text, None)
        case BlockType.CODE:
            code_block = block.lstrip("\n`")
            code_block = code_block.rstrip("`")
            code_text = TextNode(code_block, TextType.CODE, None)
            child = text_node_to_html_node(code_text)
            return ParentNode("pre", [child], None)
        case BlockType.QUOTE:
            stripped_block = []
            for line in block.split("\n"):
                stripped_block.append(line.lstrip(">").lstrip(" "))
            stripped_block_string = "<br>".join(stripped_block)

            child = TextNode(stripped_block_string, TextType.TEXT)
            child = text_node_to_html_node(child)

            return ParentNode("blockquote", [child], None)
        case BlockType.UNORDERED_LIST:
            items_list: list[str] = block.split("\n")
            sub_parents: list[ParentNode] | None = []
            for i in items_list:
                i = i[2:]
                sub_parents.append(ParentNode("li", text_to_children(i), None))
            return ParentNode("ul", sub_parents, None)
        case BlockType.ORDERED_LIST:
            items_list: list[str] = block.split("\n")
            sub_parents: list[ParentNode] | None = []
            for i in items_list:
                i = i[3:]
                sub_parents.append(ParentNode("li", text_to_children(i), None))
            return ParentNode("ol", sub_parents, None)


def markdown_to_html_node(markdown: str) -> HTMLNode:
    markdown_blocks: list[str] = markdown_to_blocks(markdown)
    content_nodes = []
    for mblock in markdown_blocks:
        content_nodes.append(block_to_html_node(mblock))
    base_node = ParentNode(
        "div",
        content_nodes,
    )
    return base_node
