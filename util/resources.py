import qtpy.QtCore as QtCore
from qtpy.QtCore import QDir
from typing import List, Dict
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import resource_rc
# import icons_rc


def extract_file_from_resource(resource_path: str, destination_path: str = None) -> str:
    """
    Extracts a file from the resource directory to a specified destination path.

    :param resource_path: The path to the resource file in the resource directory.
    :param destination_path: The path where the file should be extracted. If None, uses the current working directory.
    :return: The path to the extracted file.
    """
    file = QtCore.QFile(resource_path)

    if not file.exists():
        raise FileNotFoundError(f"Resource file not found: {resource_path}")
    if not file.open(QtCore.QFile.ReadOnly):
        raise IOError(f"Cannot open resource file: {resource_path}")

    data = file.readAll()
    file.close()

    if destination_path is None:
        # Use the current working directory as the default destination path
        destination_path = os.path.join(os.getcwd(), os.path.basename(resource_path))

    with open(destination_path, 'wb') as dest_file:
        dest_file.write(data.data())

    return destination_path


def list_resource_directory_files(resource_path: str) -> List[str]:
    """
    Lists all files in the resource directory and returns a list containing their information.

    :param resource_path: The path to the resource directory.
    :return: A list of dictionaries containing file information (name, path, size, type).
    """
    dir = QDir(resource_path)

    if not dir.exists():
        raise FileNotFoundError(f"Resource directory not found: {resource_path}")

    file_list = []

    for file_info in dir.entryInfoList(QDir.Files | QDir.NoDotAndDotDot | QDir.Dirs, QDir.SortFlag.DirsFirst):
        result = {}
        result["name"] = file_info.fileName()
        result["path"] = file_info.absoluteFilePath()
        result["size"] = f"{file_info.size() / 1024:.2f} KB" if file_info.size() > 0 else "0 KB"
        result["type"] = f"{'Directory' if file_info.isDir() else 'File'}"
        file_list.append(result)

    return file_list


def list_resource_directory_files_recursive(resource_path: str) -> List[Dict[str, str]]:
    """
    Lists all files in the resource directory and its subdirectories.

    :param resource_path: The path to the resource directory.
    :return: A list of dicts with keys: name, path, size, type.
    """
    qdir = QDir(resource_path)
    if not qdir.exists():
        raise FileNotFoundError(f"Resource directory not found: {resource_path}")

    files: List[Dict[str, str]] = []
    filters = QDir.Files | QDir.Dirs | QDir.NoDotAndDotDot
    sort = QDir.DirsFirst

    for info in qdir.entryInfoList(filters, sort):
        entry = {
            "name": info.fileName(),
            "path": info.absoluteFilePath(),
            "size": info.size(),
            "type": "Directory" if info.isDir() else "File",
        }
        files.append(entry)
        if info.isDir():
            # recurse into subdirectory
            files.extend(list_resource_directory_files_recursive(info.absoluteFilePath()))

    return files


if __name__ == "__main__":
    # Example usage
    resource_path = ":/resources/images/icons"
    file = f"{resource_path}/settings.ini"
    total_size = 0
    try:
        _list = list_resource_directory_files_recursive(resource_path)
        for file in _list:
            total_size += int(file["size"])
            for key, value in file.items():
                if key == "size":
                    total_size += int(value)
                print(f"\t{key}: {value}")
            print("\t", "∙" * 32, sep="")
        print(f"Files in resource directory: {resource_path} - {len(_list)} files found.")
        print(f"Total size: {total_size} bytes, {total_size / 1024:.2f} KB, {total_size / (1024 * 1024):.2f} MB")

    except Exception as e:
        print(f"Error: {e}")

    resource_files = list_resource_directory_files(resource_path)
    for resource_file in resource_files:
        print(resource_file)
