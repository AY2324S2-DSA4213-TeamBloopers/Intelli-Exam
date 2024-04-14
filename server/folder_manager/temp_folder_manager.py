import shutil
import os

class TempFolderManager:
    """
    A class for managing temporary folders for uploaded PDF files.

    Attributes:
        upload_folder (str): The absolute path to the directory where the uploaded PDF files will be stored.
    """

    def __init__(self):
        """
        Initialize the TempFolderManager object.
        """
        self.upload_folder = None

    def create_temp_folder(self):
        """
        Creates a temporary folder as a placeholder for all uploaded PDF files from the user.

        Returns:
            upload_folder (str): String of the absolute path to the directory where the uploaded PDF files will be stored.
        """
        try:
            # Gives absolute path of directory
            path = os.path.dirname(os.path.abspath(__file__))
            # Save file outside main directory in folder named "tmp"
            upload_folder = os.path.join(path.replace("/file_folder", ""), "../tmp")
            # Create directory recursively
            os.makedirs(upload_folder, exist_ok=True)
            # Add configuration path in app for "upload_folder"
            self.upload_folder = upload_folder
            return upload_folder
        except Exception as e:
            return "Folder could not be created"

    def remove_temp_folder(self):
        """
        Deletes the temporary folder containing all uploaded PDF files from the user.
        """
        if self.upload_folder:
            shutil.rmtree(self.upload_folder)
            self.upload_folder = None