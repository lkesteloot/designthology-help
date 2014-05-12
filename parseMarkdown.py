import markdown
import os
import codecs

header = """<head>
        <title>designthology</title>
        <link rel="stylesheet" type="text/css" href="/static/css/home.css">
        <link rel="shortcut icon" href="/static/favicon.ico?fd00191b7d" type="image/x-icon">
        <link rel="icon" href="/static/favicon.ico?fd00191b7d" type="image/x-icon">
    </head>"""

footer = """<footer>
            <h2>Designthology</h2>
            <p>&copy; 2013</p>
            <a href="mailto:jennifer@designthology.com">Contact Us</a>
        </footer>"""

def createHTMLHeirarchy(init, destination):
    for root, dirs, files in os.walk(init):
        for name in files:
            split = os.path.splitext(name)
            if split[1] == ".md":
                createHTMLFile(root, split[0], destination)

def parseMarkdown(file):
    text = codecs.open(file, 'r', encoding = 'utf8')
    return markdown.markdown(text.read())

#Takes a markdown file and 
#creates a designthology html file.
def createHTMLFile(root, baseName, destination):
    if not os.path.exists(destination + root):
        os.makedirs(destination + root)

    html = parseMarkdown(root + baseName + ".md")
    #print(html)
    file = open(destination + root + baseName + ".html", 'w')
    file.write(header)
    file.write(html)
    file.write(footer)

createHTMLHeirarchy("./", "./new/")