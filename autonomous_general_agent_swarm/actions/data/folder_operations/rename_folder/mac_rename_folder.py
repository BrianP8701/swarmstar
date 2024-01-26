import os


def mac_rename_folder(folder_path, new_folder_path):
    try:
        os.rename(folder_path, new_folder_path)
        return {'status_message': 'Success', 'error_message': ''}
    except Exception as e:
        return {'status_message': 'Failure', 'error_message': str(e)}


if __name__ == '__main__':
    # Example usage:
    # folder_path = '/path/to/old_folder'
    # new_folder_path = '/path/to/new_folder'
    # result = mac_rename_folder(folder_path, new_folder_path)
    # print(result)
    pass
