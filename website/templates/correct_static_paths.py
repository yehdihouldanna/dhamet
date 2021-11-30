import re 
from glob import glob
import argparse
try :
    from termcolor import cprint
except:
    pass

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('-f','--file', type = str , metavar='', help="the path of the file")
group.add_argument('-d','--directory',  type = str, metavar='', help= "directory containing files")
parser.add_argument('-e','--extensions',type=list, metavar='' , help= "list containing extensions, to modify , default=['html']")
parser.add_argument('-r','--rec', action="store_true", help="if to go recursively on the folder")
parser.add_argument('-v','--verbose', action="store_true", help="print file parsing success")
parser.parse_args()

def replace_patterns_in_line(line):
    insert_static = True
    """ replaces tha pattern in a line"""
    # line  = re.sub("{% static assets", "{% static assets", line)

    start = "{%% static '"
    end = "' %}"

    ## The following line matches 2 groupes (url_path that starts with assets (g1) and extension (g2) and replace it by adding {% static %} around it)
    line = re.sub(r"(assets\/[a-zA-Z0-9-,_,\/,.]+)(.css|.svg|.png|.js|.jpg|.ico)", start+r"\1"+r"\2"+end,line)
    

    ## due to the "% s" being an escape caracter we need to replace it by %% s and then treat the %%
    line = re.sub(r"%%","%",line)
    line  = re.sub('../../demo6/dist/','',line)

    if insert_static:
        text = """<meta charset="utf-8" />"""

        text_sub = """{% load static %} \n
        {% csrf_token %} \n 
		<meta charset="utf-8" />"""

        line = re.sub(text,text_sub,line)
    return line

def replace_file(file ,verbose = None):
    """replaces the patterns in the file """
    # print(f"Trying to replace the patterns in : [{file}]")
    changed = False
    with open(file,'r',encoding="utf8") as f:
        newlines = []
        for line in f.readlines():
            new_line = replace_patterns_in_line(line)
            newlines.append(new_line)
            if new_line !=line:
                changed=True
    with open(file, 'w' , encoding="utf8") as f:
        for line in newlines:
            f.write(line)

    if verbose and changed:
        try:
            cprint("Applied changes to file [", color ="blue",end =" ")
            cprint(file,color ="green",end=" ")
            cprint("] ", color ="blue")
        except Exception as e:
            # print(e)
            print(f"Applied changes to file [{file}]")
    return [0,1][changed]


if __name__ =='__main__':
    args = parser.parse_args()
    file = args.file
    dir_ = args.directory
    ver  = args.verbose
    ver = True
    rec  = args.rec
    extensions = args.extensions
    if extensions is None:
        extensions=["html"]

    count_modified = 0
    if file is None and dir_ is None:
        e = input("Do you want to parse files in the current directory [y/n] : ")
        if e =='n':
            print("You can add arguments with '-f file_name' or '-d directory' ")
            exit()
        else :
            dir_ = "."
            e = input("Do you want to apply changes recursively [y/n] : ")
            if e =="y":
                rec = True
            else :
                rec = False

    if file:
        count_modified +=replace_file(file,ver)
    else :
        files = []
        for ext in extensions:
            if rec:
                files += glob(dir_+"/**/*."+ext,recursive = True)
            else :
                files += glob(dir_+"/*."+ext)
        
        for file in files:
            count_modified +=replace_file(file,ver)
        
    try:
        cprint("[{}] files changed!".format(count_modified),color ="green")
    except:
        print("[{}] files changed!".format(count_modified))
