import PyPDF2
import os
import re


# functions
def FindText(xFile, xString):
    # xfile : the PDF file in which to look
    # xString : the string to look for
    PageFound = -10
    ramps = open(xFile, 'rb')
    pdfDoc = PyPDF2.PdfFileReader(ramps)
    for i in range(0, pdfDoc.numPages):
        content = ""
        content += pdfDoc.getPage(i).extractText() + "\n"
        ResSearch = re.search(xString, content)
        if ResSearch != None:
            PageFound = i + 1
            print('Finding text \'', xString, '\' in file ', xFile, ' .It is found in page no.: ',
                  PageFound, '\n')
            return i
    return -10


# All Variables
toadd = ''
# Path = 'E:\\STUDY\\2nd year\\ps1\\start\\files'
Path = os.path.abspath('filesk')
os.chdir(Path)
path_to_download = Path + toadd
listoffolders = list()
Output1 = PyPDF2.PdfFileWriter()

# Program Start
print('start')
##	Getting list of folders with pdf files
for dirpath, subdirs, files in os.walk(Path):
    for f in files:
        listoffolders += [dirpath]

k = set(listoffolders)
listoffolders = list(k)

print('list of folders taken :>  <3')
##	LOOP: Changing to required folder, checking if file is pdf, opening it, checking if book reviw, adding pages to pdf writer 
for dire in listoffolders:
    os.chdir(dire)
    files = [f for f in os.listdir(dire) if os.path.isfile(os.path.join(dire, f))]
    print(files)
    # exit(1)
    for file in files:
        if file.endswith(".pdf") == True:
            if FindText(file, 'BOOK REVIEWS') != -10:
                break
            pdfFileObj = open(file, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            for pageNum in range(0, 1):
                pageObj = pdfReader.getPage(pageNum)
                Output1.addPage(pageObj)
            found_page = FindText(file, 'Reference')
            # if found_page == -10:
            #     continue
            try:
                for pageNum in range(found_page, pdfReader.numPages):
                    print(pdfReader.numPages)
                    pageObj = pdfReader.getPage(pageNum)
                    Output1.addPage(pageObj)
            except:
                print(dire)
                print(files)
                print(file)
                exit(10)

        print('appended ', file, '\n')
    print('done with ', dire, '\n')

# saving the required pages as pdf
os.chdir(os.path.expanduser('~/Desktop/'))
pdfOutput1 = open('write_pdffile.pdf', 'wb')
Output1.write(pdfOutput1)
print('check desktop for Output1')
pdfOutput1.close()
