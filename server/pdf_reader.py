
from pdfminer.high_level import extract_text

class PdfReader:

    def get_text(self, file_name): 
        text = extract_text(file_name)

        return text

test = PdfReader()
text = test.get_text("StrengthsProfile-Jennifer-Chue.pdf")
text = text.replace("\n", " ")
print(text)

# remove stop words?
'''
from pypdf import PdfReader, PdfMerger

reader = PdfReader("C:/Users/jenni/Desktop/NUS/Y3S2/DSA4213/project/Intelli-Exam/server/04 - Containerization (Addendum).pdf")
page = reader.pages[0]
text = page.extract_text()
print(text)
'''