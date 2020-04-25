import os
from PyPDF2 import PdfFileMerger, PdfFileReader

fs = []
merger = PdfFileMerger()
os.chdir('files')

for (root, dirs, files) in os.walk('.', topdown=True):
    print('ier')
    fs.append(files)
    print(files)
    for file in files:
        merger.append(PdfFileReader(file, 'rb'))

merger.write("2014to2017merged.pdf")
merger.close()