#install using pip or easy_install:
#$ pip install markdown
#current version 2.4
import markdown
import os
import codecs
import sys

header = """<!DOCTYPE html><html><head>
        <title>designthology</title>
        <link rel="stylesheet" type="text/css" href="/static/css/home.css">
        <link rel="shortcut icon" href="/static/favicon.ico?fd00191b7d" type="image/x-icon">
        <link rel="icon" href="/static/favicon.ico?fd00191b7d" type="image/x-icon">
    </head><body>"""

footer = """</body></html>"""

def createHTMLHeirarchy(init, destination):
    for root, dirs, files in os.walk(init):
        for name in files:
            basename, extension = os.path.splitext(name)
            if extension == ".md":
                createHTMLFile(root, basename, destination)

def parseMarkdown(file):
    text = codecs.open(file, 'r', encoding = 'utf8')
    return markdown.markdown(text.read(), ["toc", "smarty"])

#Takes a markdown file and 
#creates a designthology html file.
def createHTMLFile(root, baseName, destination):
    pathname = os.path.join(destination, root)
    if not os.path.exists(pathname):
        os.makedirs(pathname)

    input_pathname = os.path.join(root, baseName + ".md")
    output_pathname = os.path.join(destination, root, baseName + ".html")

    html = parseMarkdown(input_pathname)
    file = open(output_pathname, 'w')
    file.write(header)
    file.write(html)
    file.write(footer)
    file.close()

createHTMLHeirarchy(sys.argv[1], sys.argv[2])
