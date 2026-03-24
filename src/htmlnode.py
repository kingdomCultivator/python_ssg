# htmlnode.py


class HTMLNode:
    def __init__(
        self,
        tag=None,
        value: str | None = None,
        children: list | None = None,
        props: dict | None = None,
    ):
        self.tag: str | None = tag  # string of tag name
        self.value: str | None = value  # innertext
        self.children: list[LeafNode] | list[HTMLNode] | None = (
            children  # HTML Children nodes
        )
        self.props: dict | None = props  # dict of html attributes

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        else:
            output = ""
            for k in self.props.keys():
                output += f' {k}="{self.props[k]}"'
            return output

    def __eq__(self, other_node) -> bool:
        if self.__repr__() == other_node.__repr__():
            return True
        else:
            return False

    def __repr__(self) -> str:
        return f"\nHTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: dict | None = None,
    ):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}>"
        elif not self.value:
            print(self.__repr__())
            raise ValueError("All leaf nodes must have a value")
        elif not self.tag:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"\n    LeafNode(tag={self.tag}, value={self.value}, props={self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("All parent nodes must have a tag")
        elif not self.children:
            raise ValueError("All parent nodes must have children")
        else:
            children_strings = ""
            for child in self.children:
                children_strings += child.to_html()
            return f"<{self.tag}{self.props_to_html()}>{children_strings}</{self.tag}>"

    def __repr__(self) -> str:
        return f"\nParentNode(tag={self.tag}, children={self.children}, props={self.props})"
