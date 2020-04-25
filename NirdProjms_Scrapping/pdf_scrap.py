import PyPDF2
import textract

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


file_path = '/home/sriteja/PycharmProjects/NirdProjms_Scrapping/files/2017/Volume 36, Issue 1, January-March 2017/112698-255599-1-SM.pdf'

pdfFileObj = open(file_path,'rb')

pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

num_pages = pdfReader.numPages

count = 0
text = ""

while count < num_pages:
    pageObj = pdfReader.getPage(count)
    count +=1
    text += pageObj.extractText()

if text == "":
    text = textract.process(file_path, method='tesseract', language='eng')

tokens = word_tokenize(text)

punctuations = ['(',')',';',':','[',']',',']

stop_words = stopwords.words('english')
keywords = [word for word in tokens if not word in stop_words and not word in punctuations]