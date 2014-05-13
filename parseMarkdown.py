#install using pip or easy_install:
#$ pip install markdown
#current version 2.4
import markdown
import os
import codecs
import sys

header = """<!DOCTYPE html>
<html>
    <head>
        <title>designthology help</title>
        <link rel="stylesheet" href="/static/css/idwebtool.css">
        <link rel="stylesheet" href="/static/css/bootstrap.css">
        <link rel="stylesheet" href="/static/font-awesome/css/font-awesome.min.css">
        <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body id="help_page">
        <div role="navigation" class="navbar navbar-inverse navbar-fixed-top">
            <div class="navbar-header">
                <a class="navbar-brand" href="/">designthology</a>
            </div>
        </div>
         <div class="container">
"""

footer = """        </div>
        <script>
          (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
          (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
          m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
          })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
          ga('create', 'UA-50725304-1', 'designthology.com');
          ga('send', 'pageview');
        </script>
    </body>
</html>"""

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
