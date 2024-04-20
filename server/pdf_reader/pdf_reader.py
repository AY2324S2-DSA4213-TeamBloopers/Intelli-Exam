from pdfminer.high_level import extract_text

class PdfReader:
    """
    A class to read a pdf and process its texts
    """

    def get_text(self, file_name, input_type): 
        """
        Extracts the texts from the pdf 

        Args:
            file_name (str): The path to the pdf file to extract text from.
            input_type (str): The type of input from the pdf file that the user uploaded. It is either "format" or "context".

        Returns:
            result (list[str]): List of strings that has been extracted from the pdf file. 
        """

        text = extract_text(file_name).strip()
        if input_type == "format":
            # Return the text in the pdf file as chunks of 200, potentially capturing all the questions in the pdf
            return [text[i:i+200] for i in range(0, len(text), 200)]

        if input_type == "context":
            # Return the text in the pdf file that has been split and filtered of minimum char length of 55 for substantial chunks of information for referencing
            return [x.replace("\n", " ") for x in text.split("\n\n") if len(x) > 55]

        # Input_type out of scope if code has reached here
        raise TypeError("Your input_type must be either 'format' or 'context'.")
    