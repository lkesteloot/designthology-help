class HTMLFile:
    '''
    pathname is the full path of the file
    markdown_header is the the metadata from the
                    markdiwn file.
    '''
    def __init__(self, pathname, basename, markdown_header, text):
        self.pathname = pathname
        self.basename = basename
        self.markdown_header = markdown_header
        self.text = text