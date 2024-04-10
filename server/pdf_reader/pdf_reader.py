from pdfminer.high_level import extract_text

class PdfReader:
    """
    A class to read a pdf 
    """

    def get_text(self, file_name): 
        """
        Extracts the texts from the pdf 

        Args: 
            file_name (str): The path to the pdf file to extract text from.

        Returns:
            result (list[str]): List of strings that has been extracted from the pdf file. 
        """
        text = extract_text(file_name).strip().split("\n\n")
        text = list(filter(lambda x: len(x) > 55, text))
        return text