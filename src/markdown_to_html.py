from inline import *
from blocktype import *
import textwrap

def markdown_to_html_node(markdown):
    node_tree_parent = []
    parents = []
    ## markdown gets divided by \n\n
    markdown_blocks = markdown_to_blocks(markdown)

    for block in markdown_blocks:
        
        # we get the type of the block
        block_type = block_to_block_type(block)
        
        # get block stripped by start/endline and the tag
        strip_block,tag = from_block_to_tag_and_strip(block, block_type)

        #We cycle through the lines of the lists to make the lines children list
        if block_type == BlockType.unordered_list or block_type == BlockType.ordered_list:
            children = []
            for strip_bit in strip_block:
                line_child = ParentNode('li',text_to_children(strip_bit))
                children.append(line_child)

        #we handle now the code exception
        elif tag == 'pre':
            if strip_block.startswith("\n"):
                #we remove the first newline
                strip_block = strip_block[1:]
            #we remove the indentation from the node block
            dedent_block = textwrap.dedent(strip_block)
            #We create manually the textnode
            code_text_node = TextNode(dedent_block,TextType.TEXT)

            #we make the children like before and we wrap it so it's considered a list
            code_grandchild = [text_node_to_html_node(code_text_node)]
            children = [ParentNode('code',code_grandchild)]

        else:
            # we get HTML leaf nodes
            children = text_to_children(strip_block)
            


        #we then make the parent node that gets the children
        parent = ParentNode(tag, children)
        parents.append(parent)

    node_tree_parent = ParentNode('div',parents)
    return node_tree_parent


def text_to_children(text):

    html_nodes = []

    #we convert the text to textnodes
    text_nodes = text_to_textnodes(text)

    #we loop over the text nodes and we convert them to html
    for text_node in text_nodes:
        #the if cycle is to avoid to process empty texnodes
        if text_node.text != "":
            #we convert the textnode to html node
            html_node = text_node_to_html_node(text_node)
            #we add the html node to out final list
            html_nodes.append(html_node)

    return html_nodes


def from_block_to_tag_and_strip(block,block_type):
    match block_type:
        case BlockType.paragraph:
            lines = block.split("\n")
            clean_lines = [line.strip() for line in lines]
            new_block = " ".join(clean_lines)
            tag = 'p'
            return new_block,tag

        case BlockType.heading:
            i = 0
            while block[i] == '#':
                i += 1
            new_block = block[i+1:]
            tag = f'h{i}'
            return new_block,tag

        case BlockType.code:
            ## need to double check if I need to strip also the \n from it
            new_block = block[3:-3]
            tag = 'pre'
            return new_block,tag

        case BlockType.quote:
            split_block = block.split('\n')
            quote_lines = []
            for block in split_block:
                if len(block) > 1 and block[1] == ' ':
                    quote_lines.append(block[2:])

                else:
                    quote_lines.append(block[1:])

            new_block = " ".join(quote_lines)

            tag = 'blockquote'
            return new_block,tag

        case BlockType.unordered_list:
            split_block = block.split('\n')
            new_block = []
            for i in range(len(split_block)):
                new_block.append(split_block[i][2:])
            tag = "ul"
            return new_block,tag
        
        case BlockType.ordered_list:
            split_block = block.split('\n')
            new_block = []
            for i in range(len(split_block)):
                new_block.append(split_block[i][3:])
            tag = "ol"
            return new_block,tag

        case _:
            raise ValueError("BlockType doesnt match with block_type keys")

