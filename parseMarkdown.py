#install using pip or easy_install:
#$ pip install markdown
#current version 2.4
import markdown
import os
import codecs
import sys
import HTMLFile
import glob

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
            <div class="row">
                <div class="col-md-3">
                    <div class="tableOfContents">
                        <h1>Help</h1>
"""

separator = '''</div></div><div class="col-md-9">'''
footer = """        </div>
        </div>
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
    global header
    md_files = glob.glob(os.path.join(init, '*.md'))
    html_files = []

    for markdownFile in md_files:
        basename, extension = os.path.splitext(markdownFile)
        html_files.append(createHTMLFile(init, basename, destination))

    #sort files based on order attribute in markdown meta-data
    html_files.sort(key = lambda k: int(k.markdown_header.get(u'order', ["0"])[0]))
    writeFiles(html_files)

#def createHTMLHeirarchy(init, destination):
    #global header
    #html_files = []
    ##walk the directory tree
    ##   for each file in directory
    ##       if file is a markdown file
    ##           create an html file in corresponding destination directory
    ##           push file to html_files list
    #for root, dirs, files in os.walk(init):
        #for name in files:
            #basename, extension = os.path.splitext(name)
            #if extension == ".md":
                #html_files.append(createHTMLFile(root, basename, destination))
    #contents_div = '''<div class="contents"><ul>'''
#
    ##sort files based on order attribute in markdown meta-data
    #sorted(html_files, key = lambda k: int(k.markdown_header.get(u'order', ["0"])[0]))
#
    ##adding titles to contents as an unordered list
    #for file in html_files:
        #contents_div += '''<li><a href="''' + file.pathname + '''">''' + file.markdown_header.get(u'title', ["Untitled"])[0] + '''</a></li>'''
#
    #contents_div += '''</ul></div>'''
    #header += contents_div
    #writeFiles(html_files)

#uses markdown module to parse markdown file into html file
#and markdown meta-data
#see http://pythonhosted.org/Markdown/extensions/meta_data.html
#for markdown header specification
def parseMarkdown(file):
    f = codecs.open(file, 'r', encoding = 'utf8')
    md = markdown.Markdown(extensions = ["smarty", "meta"])
    text = md.convert(f.read())
    return [md.Meta, text]

#Takes a markdown file and 
#creates a designthology html file.
#returns an HTMLFile object
def createHTMLFile(root, baseName, destination):
    pathname = os.path.join(destination, root)
    if not os.path.exists(pathname):
        os.makedirs(pathname)

    input_pathname = os.path.join(root, baseName + ".md")
    output_pathname = os.path.join(destination, baseName + ".html")

    markdown_header, html = parseMarkdown(input_pathname)
    return HTMLFile.HTMLFile(output_pathname, baseName + ".html", markdown_header, html)

def generateToc(html_files, html_file):
    toc = '''<ul>'''

    #adding titles to contents as an unordered list
    for file in html_files:
        filename = os.path.basename(file.basename)
        title = file.markdown_header.get(u'title', ["Untitled"])[0]

        toc += '''<li'''
        if file is html_file:
            toc += ''' class="currentHelpPage"'''
        toc += '''><a href="''' + filename + '''">''' + title + '''</a></li>'''

    toc += '''</ul>'''

    return toc

#file_array is an array of HTMLFile objects
def writeFiles(file_array):
    for html_file in file_array:
        file = open(html_file.pathname, 'w')
        file.write(header)
        file.write(generateToc(file_array, html_file))
        file.write(separator)
        file.write(html_file.text)
        file.write(footer)
        file.close()

createHTMLHeirarchy(sys.argv[1], sys.argv[2])
