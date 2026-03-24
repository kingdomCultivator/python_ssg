# main.py
import sys
import os
import shutil
from markdown_to_blocks import markdown_to_html_node

basepath = "/"
if len(sys.argv) > 1:
    basepath = sys.argv[1]

# from textnode import TextNode, TextType


def copy_static(src, dest):
    src = os.path.abspath(src)
    dest = os.path.abspath(dest)
    print(f"\nCopyStatic\ncopying files from {src} to {dest}\n")
    if os.path.exists(dest):
        if os.path.isdir(dest):
            shutil.rmtree(dest)
            os.mkdir(dest)
        else:
            raise FileExistsError(f"{dest} is a file, not a directory")
    else:
        os.mkdir(dest)

    for path in os.listdir(src):
        path = os.path.join(src, path)
        dest_node = os.path.abspath(os.path.join(dest, os.path.basename(path)))
        if os.path.isdir(path):
            print(f"moving into directory {dest_node}")
            os.mkdir(dest_node)
            copy_static(path, dest_node)
        else:
            print(f"copying file {path} to {dest_node}")
            shutil.copy(path, dest_node)


def extract_title(markdown: str):
    if markdown.startswith("# "):
        first_line = markdown.split("\n")[0].removeprefix("# ").strip()
        return first_line
    else:
        raise Exception("Markdown file must begin with a heading")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as from_file:
        markdown = from_file.read()
        with open(template_path) as template_file:
            html_string = markdown_to_html_node(markdown)
            # print(f"html string after markdown to node:\n\n{html_string}")
            html_string = html_string.to_html()
            title = extract_title(markdown)
            template = template_file.read()
            output_string = (
                template.replace("{{ Title }}", title)
                .replace("{{ Content }}", html_string)
                .replace('href="/', f'href="{basepath}')
                .replace('src="/', f'src="{basepath}')
            )
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, mode="x") as new_file:
                new_file.write(output_string)


def generate_pages_recursive(dir_path_content, template_path, dest_dir, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir, from_path)
        if os.path.isfile(from_path):
            dest_path = dest_path.replace("content/", "")
            if from_path.endswith(".md"):
                dest_path = dest_path.replace(".md", ".html")
                generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_dir, basepath)


def main():
    copy_static("static", "docs")
    generate_pages_recursive("content/", "template.html", "docs/", basepath)


if __name__ == "__main__":
    main()
