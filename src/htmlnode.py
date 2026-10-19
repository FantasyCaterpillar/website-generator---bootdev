class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag #HTML tag name (p, h1 etc.)
        #if none it renders raw text
        self.value = value # Ex text inside the paragraph
        #if none it will have children
        self.children = children #List of HTML node objects representing the children of this node
        #if none it has got a value
        self.props = props # dictionary of key value pairs representing the attributes of the html tag like href : https://google.com
        #if none it hasn't got attributes

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        props_list = ""
        
        #we check if the dictionary is empty or not
        if self.props:
            #if not empty we cycle through it's elements and we return them in a different format
            for key,value in self.props.items():
                props_list += f' {key}="{value}"'

                    
            return props_list

        else:
            return props_list

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'  

class LeafNode(HTMLNode):
    # it shouldn't allow for any children
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)
    
    def to_html(self):

        if self.tag == "img":
            props = self.props_to_html()
            result = f"<img {props}/>"
            return result

        if not self.value:
            raise ValueError("Invalid HTML: no Value")
        
        elif not self.tag:
            return self.value

        # it should render the node as an HTML tag
        # For example
        # LeafNode("p", "This is a paragraph of text.").to_html()
        # "<p>This is a paragraph of text.</p>"
        else:
            props = self.props_to_html()
            result = f"<{self.tag}{props}>{self.value}</{self.tag}>"
            return result



    def __repr__(self):
            return f'LeafNode({self.tag}, {self.value}, {self.props})' 

class ParentNode(HTMLNode):
    # it shouldn't allow for any children
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):

        if not self.tag:
            raise ValueError('Missing tag from Parent Node')

        if not self.children:
                raise ValueError('Missing children from Parent Node')

        else:
            props = self.props_to_html()
            children_list = ""
            for i in range(len(self.children)):
                child = self.children[i].to_html()
                children_list += child

            return f"<{self.tag}{props}>" + children_list + f"</{self.tag}>"
            
            

#node = LeafNode("p", "").to_html()
#print(f'the node value is {node.value}')

