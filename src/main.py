from textnode import *
from markdown_to_html import *
from inline import *
import sys
import os
import shutil


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = '/'

    print(os.getcwd())
    copy_and_paste('static','docs')

    #we now generate a page
    generate_website('content', 'template.html', 'docs', basepath)

def generate_website(from_path, template_path, dest_path, basepath):

    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    
    #we list the content of the directory   
    list_from_dir = os.listdir(from_path)

    #we cycle through the content of the directory
    for list_entry in list_from_dir:

        # if the list entry is a file we have to transform it
        if os.path.isfile(os.path.join(from_path, list_entry)):
            #we filter out the digital junk
            if list_entry.endswith(".md"):
                generate_page(os.path.join(from_path, list_entry), template_path, dest_path, basepath)

        #if instead it's a directory we need to:
        else:
            new_dest_path = os.path.join(dest_path, list_entry)
            #1.1 if it exists already we remove the old directory and we recreate it again
            if os.path.exists(new_dest_path):
                #Delete entries from the destination dir
                shutil.rmtree(new_dest_path)
                #we remake the destination directory
                os.mkdir(new_dest_path)
            else:
            #1.2 create the new directory inside of dest path if it doesn't exist
                # if it doesn't exist then we create it
                os.mkdir(new_dest_path)

            #2. recursively call generate website with the new from and dest paths
            generate_website(os.path.join(from_path, list_entry), template_path, new_dest_path, basepath)

def generate_page(file_path, template_path, dest_path, basepath):

    #open the given file path and store the content inside of markdown_r
    with open(f"{file_path}") as f:
        markdown_r = f.read()

    #open and read the from template path and store the content inside of template_r
    with open(f"{template_path}") as g:
        template_r = g.read()

    #we convert the markdown to html nodes first and then to string
    html_node = (markdown_to_html_node(markdown_r))
    html_string = html_node.to_html()
    

    #we extract the title of the markdown
    title_markdown = extract_title(markdown_r)

    #replace the title and content placeholder inside of the template with the markdown title and html string
    mod_template = (
        template_r
            .replace('{{ Title }}', f'{title_markdown}')
            .replace('{{ Content }}', f'{html_string}')
            .replace('href="/', f'href="{basepath}')
            .replace('src="/', f'src="{basepath}')
    )

#write the new html page at the dest_path
    print(f'destination path is {dest_path}, file path is {file_path} ')
    html_path = os.path.join(dest_path,'index.html')
    #we write to the destination path, the name of the new file is chosen by the new path
    # open will make the file with the "w" function
    with open(f"{html_path}","w") as j:
        j.write(f"{mod_template}")

 ## Recursive function that copies and paste all the contents from a source directory to a destination directory
def copy_and_paste(source_dir, destination_dir):
    # if the path already exist we wipe it and make it from scratch
    if os.path.exists(destination_dir):
        #Delete entries from the destination dir
        shutil.rmtree(destination_dir)
        #we remake the destination directory
        os.mkdir(destination_dir)
    else:
    # if it doesn't exist then we create it
        os.mkdir(destination_dir)

    #We check that the source path exists
    if os.path.exists(source_dir):

        copied_elements = []
        #list of all the files in the source directory
        list_source_dir = os.listdir(source_dir)
        #We then cycle through the elements inside of the directory and divide directories and files
        for list_entry in list_source_dir:
            #If the entry is a file then we copy it and we add to our list of copied items
            if os.path.isfile(os.path.join(source_dir, list_entry)):
                shutil.copy(os.path.join(source_dir, list_entry), destination_dir)
                copied_elements.append(os.path.join(source_dir, list_entry))
            else:
                #If it's not a file then it's a directory, we create a new one
                os.mkdir(os.path.join(destination_dir, list_entry))
                #we change the current source and destination directories and we recursively run the code with the new directories
                new_source_dir = os.path.join(source_dir, list_entry)
                new_destination_dir = os.path.join(destination_dir, list_entry)
                copied_elements.append(new_destination_dir)
                copied_elements.append(copy_and_paste(new_source_dir, new_destination_dir))
        print(f'copied elements at the moment are {copied_elements}')
        return copied_elements


    else:
        ValueError("Source directory path doesn't exist")

        
    
    
    #It should then copy all files and subdirectories
    
    #Log everytime you copy something so it's easy to dobug I would say also log what you delete

    
main()