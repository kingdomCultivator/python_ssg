# textnode.py
import re
from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "TEXT"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    CODE = "CODE"
    LINK = "LINK"
    IMAGE = "IMAGE"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_node):
        if self.__repr__() == other_node.__repr__():
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("TextNode must have valid TextType attribute")


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode] | list:
    output_nodes = []
    for o_node in old_nodes:
        if o_node.text_type != TextType.TEXT:
            output_nodes.append(o_node)
        elif delimiter in o_node.text:
            hopper = o_node.text.split(delimiter)
            if len(hopper) % 2 == 0:
                raise Exception("Invalid markdown: unmatched delimiters")
            else:
                for i in range(len(hopper)):
                    if hopper[i] == "":
                        continue
                    if i == 0 or i % 2 == 0:
                        output_nodes.append(TextNode(hopper[i], TextType.TEXT))
                    else:
                        output_nodes.append(TextNode(hopper[i], text_type))
        else:
            output_nodes.append(o_node)
    return output_nodes


def text_to_textnodes(text: str) -> list[TextNode] | list:
    delimiter_tuples = [
        ("**", TextType.BOLD),
        ("_", TextType.ITALIC),
        ("`", TextType.CODE),
    ]
    init_node = TextNode(text, TextType.TEXT, None)
    out_nodes = [init_node]
    for d, t in delimiter_tuples:
        out_nodes = split_nodes_delimiter(out_nodes, d, t)
    out_nodes = split_nodes_image(out_nodes)
    out_nodes = split_nodes_link(out_nodes)
    return out_nodes


def extract_markdown_links(text: str):
    extract_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(extract_regex, text)
    return matches


def split_nodes_link(nodes):
    output_nodes = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            formatted_nodes: list[TextNode] | None = []
            matches = extract_markdown_links(node.text)
            if len(matches) > 0:
                matches_nodes = [
                    TextNode(link_tuple[0], TextType.LINK, link_tuple[1])
                    for link_tuple in matches
                ]
                for match in matches_nodes:
                    match_delimiter = f"[{match.text}]({match.url})"
                    if len(formatted_nodes) == 0:
                        split_nodes_text = node.text.split(match_delimiter, maxsplit=1)
                    else:
                        split_nodes_text = formatted_nodes.pop().text.split(
                            match_delimiter, maxsplit=1
                        )
                    first_node = TextNode(split_nodes_text[0], TextType.TEXT, None)
                    second_node = TextNode(split_nodes_text[1], TextType.TEXT, None)
                    working_nodes = [first_node, match, second_node]

                    for wn in working_nodes:
                        if len(wn.text) > 0:
                            formatted_nodes.append(wn)

                output_nodes.extend(formatted_nodes)
            else:
                output_nodes.append(node)
        else:
            output_nodes.append(node)

    return output_nodes


def extract_markdown_images(text: str) -> list[tuple] | list:
    extract_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(extract_regex, text)
    return matches


def split_nodes_image(nodes: list[TextNode]) -> list[TextNode]:
    output_nodes: list[TextNode] | list[None] = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            formatted_nodes: list[TextNode] | None = []
            matches = extract_markdown_images(node.text)
            if len(matches) > 0:
                matches_nodes = [
                    TextNode(link_tuple[0], TextType.IMAGE, link_tuple[1])
                    for link_tuple in matches
                ]
                for match in matches_nodes:
                    match_delimiter = f"![{match.text}]({match.url})"
                    if len(formatted_nodes) == 0:
                        split_nodes_text = node.text.split(match_delimiter, maxsplit=1)
                    else:
                        split_nodes_text = formatted_nodes.pop().text.split(
                            match_delimiter, maxsplit=1
                        )
                    first_node = TextNode(split_nodes_text[0], TextType.TEXT, None)
                    second_node = TextNode(split_nodes_text[1], TextType.TEXT, None)
                    working_nodes = [first_node, match, second_node]

                    for wn in working_nodes:
                        if len(wn.text) > 0:
                            formatted_nodes.append(wn)

                output_nodes.extend(formatted_nodes)
            else:
                output_nodes.append(node)
        else:
            output_nodes.append(node)

    return output_nodes


def text_to_children(text: str) -> list[LeafNode]:
    leaf_nodes: list[LeafNode] | None = []
    text_nodes: list[TextNode] = text_to_textnodes(text)
    for n in text_nodes:
        leaf_nodes.append(text_node_to_html_node(n))
    return leaf_nodes
