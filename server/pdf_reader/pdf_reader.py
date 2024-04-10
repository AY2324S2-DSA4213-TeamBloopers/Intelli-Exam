from pdfminer.high_level import extract_text

class PdfReader:

    def get_text(self, file_name): 
        text = extract_text(file_name).strip().split("\n\n")
        text = list(filter(lambda x: len(x) > 55, text))
        return text