from typing import BinaryIO

# Placeholder for file storage upload method
def default_file_storage_upload(data: BinaryIO, name: str) -> None:
    '''
    Placeholder method for uploading files to storage.
    Users should replace this method with their own logic.

    Parameters:
        - data (binary): Binary data to be uploaded.
        - name (str): The name to be used for the stored data.
    '''
    raise NotImplementedError("Please implement the file storage upload method.")

# Placeholder for file storage retrieval method
def default_file_storage_retrieval(name: str) -> BinaryIO:
    '''
    Placeholder method for retrieving files from storage.
    Users should replace this method with their own logic.

    Parameters:
        - name (str): The name of the data to be retrieved.

    Returns:
        - data (binary): The retrieved binary data.
    '''
    raise NotImplementedError("Please implement the file storage retrieval method.")
