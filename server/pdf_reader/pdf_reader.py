from pdfminer.high_level import extract_text

import re 

class PdfReader:
    """
    A class to read a pdf 
    """

    def get_text(self, file_name, input_type): 
        """
        Extracts the texts from the pdf 

        Args: 
            file_name (str): The path to the pdf file to extract text from.
            input_type (str): The type of input from the pdf file that the user uploaded 

        Returns:
            result (list[str]): List of strings that has been extracted from the pdf file. 
        """
        
        if input_type == "sample":
            # Return the text in the pdf file as a a whole 
            text = [re.sub("(\n)+", " ", extract_text(file_name).strip())]
        else:
            # Return the text in the pdf file that has been split and filtered 
            text = extract_text(file_name).strip().split("\n\n")
            text = [x.replace("\n", " ") for x in text if len(x) > 55]

        return text