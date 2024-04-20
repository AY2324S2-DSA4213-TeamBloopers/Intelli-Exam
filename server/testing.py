from pdf_reader.pdf_reader import PdfReader

k = PdfReader()
g = k.get_text("Sample_Questions.pdf", "sample")
# for i in g:
#     print(i)
#     print("---------------")