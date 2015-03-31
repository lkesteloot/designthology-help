# install using pip or easy_install:
# $ pip install markdown
# current version 2.4
import markdown
import os
import codecs
import sys
import glob
import shutil

HEADER = """<!DOCTYPE html>
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

SEPARATOR = '''</div></div><div class="col-md-9">'''
FOOTER = """        </div>
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

IGNORED_FILES = [".git", ".gitignore"]

class HTMLFile:
    '''
    pathname is the full path of the file
    metadata is the the metadata from the markdown file.
    '''
    def __init__(self, pathname, filename, metadata, html):
        self.pathname = pathname
        self.filename = filename
        self.metadata = metadata
        self.html = html

    def getTitle(self):
        return self.metadata.get(u"title", ["Untitled"])[0]

    def getOrder(self):
        return int(self.metadata.get(u"order", ["0"])[0])

def createHTMLHierarchySingleDir(sourceDir, destinationDir):
    markdownFilenames = glob.glob(os.path.join(sourceDir, "*.md"))
    htmlFiles = []

    for markdownFilename in markdownFilenames:
        basename, extension = os.path.splitext(markdownFilename)
        htmlFiles.append(createHTMLFile(sourceDir, basename, destinationDir))

    # Sort files based on order attribute in markdown meta-data.
    htmlFiles.sort(key=lambda htmlFile: htmlFile.getOrder())
    writeFiles(htmlFiles)

# Removes filenames in-place that should be ignored.
def removeIgnoredFiles(filenames, ignoredFilenames):
    for ignoredFilename in ignoredFilenames:
        if ignoredFilename in filenames:
            filenames.remove(ignoredFilename)

def createHTMLHierarchy(sourceDir, destinationDir):
    htmlFiles = []

    ##walk the directory tree
    ##   for each file in directory
    ##       if file is a markdown file
    ##           create an html file in corresponding destination directory
    ##           push file to htmlFiles list
    for root, dirs, filenames in os.walk(sourceDir):
        removeIgnoredFiles(dirs, IGNORED_FILES)
        removeIgnoredFiles(filenames, IGNORED_FILES)

        for filename in filenames:
            basename, extension = os.path.splitext(filename)
            if extension == ".md":
                # Process Markdown.
                htmlFiles.append(createHTMLFile(root, basename, destinationDir))
            else:
                # Copy file.
                sourcePathname = os.path.join(sourceDir, root, filename)
                fullDestinationDir = os.path.join(destinationDir, root)
                shutil.copy(sourcePathname, fullDestinationDir)

    ##sort files based on order attribute in markdown meta-data
    sorted(htmlFiles, key=lambda htmlFile: htmlFile.getOrder())

    writeFiles(htmlFiles)

# uses markdown module to parse markdown file into html file
# and markdown meta-data
# see http://pythonhosted.org/Markdown/extensions/meta_data.html
# for markdown header specification
def parseMarkdown(pathname):
    f = codecs.open(pathname, "r", encoding = "utf8")
    md = markdown.Markdown(extensions = ["smarty", "meta"])
    html = md.convert(f.read())
    return md.Meta, html

#Takes a markdown file and 
#creates a designthology html file.
#returns an HTMLFile object
def createHTMLFile(root, baseName, destinationDir):
    pathname = os.path.join(destinationDir, root)
    if not os.path.exists(pathname):
        os.makedirs(pathname)

    inputPathname = os.path.join(root, baseName + ".md")
    outputFilename = baseName + ".html"
    outputPathname = os.path.join(destinationDir, root, outputFilename)

    metadata, html = parseMarkdown(inputPathname)
    return HTMLFile(outputPathname, outputFilename, metadata, html)

def generateToc(htmlFiles, htmlFile):
    toc = '''<ul>'''

    # Adding titles to contents as an unordered list.
    for tocHtmlFile in htmlFiles:
        filename = os.path.basename(tocHtmlFile.filename)
        title = tocHtmlFile.getTitle()

        toc += '''<li'''
        if tocHtmlFile is htmlFile:
            toc += ''' class="currentHelpPage"'''
        toc += '''><a href="''' + filename + '''">''' + title + '''</a></li>'''

    toc += '''</ul>'''

    return toc

#htmlFileList is an array of HTMLFile objects
def writeFiles(htmlFileList):
    for htmlFile in htmlFileList:
        writeFile(htmlFileList, htmlFile)

def writeFile(htmlFileList, htmlFile):
    f = open(htmlFile.pathname, "w")
    f.write(HEADER)
    f.write(generateToc(htmlFileList, htmlFile))
    f.write(SEPARATOR)
    f.write(htmlFile.html)
    f.write(FOOTER)
    f.close()

if __name__ == "__main__":
    createHTMLHierarchy(sys.argv[1], sys.argv[2])

