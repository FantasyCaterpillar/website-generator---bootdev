from htmlnode import *
from textnode import *

import re

#small function to remove the heading of the markdown and return the title
def extract_title(markdown):
    #we separate the first line from the rest
    split_title = (markdown.split('\n',maxsplit=1))
    #we then take the first line and strip it from the whitespace
    split_header = (split_title[0]).strip()

    #we then make sure that our header starts with #
    if split_header[0] == '#':
        return split_header[2:]
    else:
        raise Exception("No heading # present in title")
    
def markdown_to_blocks(markdown):
        splitted_markdown = markdown.split('\n\n')
        blocks_list = []
        for line in splitted_markdown:
            if line.strip() != "":
                blocks_list.append(line.strip())

        return blocks_list

def text_to_textnodes(text):

    text_node = [TextNode(text,TextType.TEXT)]

    bold_list = split_nodes_delimiter(text_node,'**',TextType.BOLD)
    italic_list = split_nodes_delimiter(bold_list,'_',TextType.ITALIC)
    code_list = split_nodes_delimiter(italic_list,'`',TextType.CODE)
    image_list = split_nodes_image(code_list)
    link_list = split_nodes_link(image_list)
    return link_list




def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_node = node.text.split(delimiter)
            if (len(split_node) % 2) == 0:
                raise ValueError(f'even number of delimiter in {node}')

            else:

                for i in range(0,len(split_node),1):
                    # if it's even we make it a normal text node
                    if i % 2 == 0:
                        new_nodes.append(TextNode(split_node[i], TextType.TEXT))

                    # if it's not then it means that is a special one
                    else:
                        new_nodes.append(TextNode(split_node[i], text_type))

                            
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    # We create the new nodes list
    # We check if the node we are checking is a TEXT TextType or not ( if not we just add it as is)
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:

            # we extract the markdown images from the node and we cycle through them
            images = extract_markdown_images(node.text)
            # if images is empty we raise Value error
            if not images:
                ## check if we want this to happen or if we want it to simply paste it again
                new_nodes.append(node)
            else:
                # we cycle through the images and we check in the node
                remaining_text = node.text
                for image in images:
                    ## maybe I will have to unpack here the tuple first let's test it
                    # we split based on the image

                    split_node = remaining_text.split(f"![{image[0]}]({image[1]})",1)
                    # I am not making a security check if there is more than one image with the same name
                    # but should be all right for the moment
                    
                    #The two parts or whatever are splitted based on our images so we need to fill the void with the image
                    
                    new_nodes.append(TextNode(split_node[0], TextType.TEXT))
                    new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    remaining_text = split_node[1]

                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    # We create the new nodes list
    # We check if the node we are checking is a TEXT TextType or not ( if not we just add it as is)
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:

            # we extract the markdown images from the node and we cycle through them
            links = extract_markdown_links(node.text)
            # if images is empty we raise Value error
            if not links:
                ## check if we want this to happen or if we want it to simply paste it again
                new_nodes.append(node)
            else:
                # we cycle through the images and we check in the node
                remaining_text = node.text
                for link in links:
                    ## maybe I will have to unpack here the tuple first let's test it
                    # we split based on the image

                    split_node = remaining_text.split(f"[{link[0]}]({link[1]})",1)
                    # I am not making a security check if there is more than one image with the same name
                    # but should be all right for the moment
                    
                    #The two parts or whatever are splitted based on our images so we need to fill the void with the image
                    new_nodes.append(TextNode(split_node[0], TextType.TEXT))
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    remaining_text = split_node[1]

                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    tuples_list = []
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for match in matches:
        new_tuple = (match)
        tuples_list.append(new_tuple)

    return tuples_list

def extract_markdown_links(text):
    tuples_list = []
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for match in matches:
        new_tuple = (match)
        tuples_list.append(new_tuple)

    return tuples_list



