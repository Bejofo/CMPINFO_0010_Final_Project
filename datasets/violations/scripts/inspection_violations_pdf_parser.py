import pdfreader
from pdfreader import PDFDocument, SimplePDFViewer

def get_numbers(pdf_file_name):
    fd = open(pdf_file_name,"rb")
    viewer = SimplePDFViewer(fd)
    viewer.render()
    contents = viewer.canvas.strings
    last_low =  len(contents) - 1 - contents[::-1].index('Low')
    ans = contents[last_low-1::2][1:5]
    if any(not x.isnumeric() for x in ans):
        return [None,None,None,None] # something went wrong
    return ans

#get_numbers("/mnt/c/Users/thxs4/Downloads/rwservlet (2).pdf")
