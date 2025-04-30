import qtpy.QtCore as QtCore
from qtpy.QtCore import QDir, QFile, QIODevice
import zipfile
import io
from typing import List, Dict
import sys
import os
import util.config_resources_rc

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
    elif os.path.exists(destination_path):    # If the destination path already exists, raise an error
        raise FileExistsError(f"Destination file already exists: {destination_path}")

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


def extract_zip_from_resources(path: str) -> None:
    """Extracts a ZIP file from the resources and extracts its contents to the specified path."""
    # Open the ZIP file stored in resources
    zip_file = QFile(":/default_resources.zip")
    if zip_file.open(QIODevice.ReadOnly):
        # Read the contents into a QByteArray
        zip_data = zip_file.readAll()
        # Use BytesIO to treat the QByteArray as a file-like objectc
        zip_file_like = io.BytesIO(zip_data)
        # Now, use the zipfile module to extract files from the ZIP archive
        with zipfile.ZipFile(zip_file_like, 'r') as zip_ref:
            # List all files in the ZIP file
            zip_ref.printdir()
            # Extract all files (you can specify a directory if you want to extract it somewhere)
            zip_ref.extractall(path)
            print("ZIP file extracted successfully.")
    else:
        print("Failed to open the ZIP file from resources.")


if __name__ == "__main__":
    # Example usage

    resource_path = ":/"  # Path to the resource file in the resource directory

    # try:
    #     list_resource_directory_files_recursive(resource_path)
    # except Exception as e:
    #     print(f"Error extracting file from resource: {e}")


    # resource_path = ":/"
    # file = f"{resource_path}/settings.ini"
    # total_size = 0
    # try:
    #     _list = list_resource_directory_files_recursive(resource_path)
    #     for file in _list:
    #         total_size += int(file["size"])
    #         for key, value in file.items():
    #             if key == "size":
    #                 total_size += int(value)
    #             print(f"\t{key}: {value}")
    #         print("\t", "∙" * 32, sep="")
    #     print(f"Files in resource directory: {resource_path} - {len(_list)} files found.")
    #     print(f"Total size: {total_size} bytes, {total_size / 1024:.2f} KB, {total_size / (1024 * 1024):.2f} MB", "\n")

    # except Exception as e:
    #     print(f"Error: {e}")
    # extract_zip_from_resources("./util/extracted_resources")  # Specify the path where you want to extract the ZIP file
    # resource_files = extract_file_from_resource(":/default_resources.zip", destination_path="./util/extracted_resources.zip")  
    # for resource_file in resource_files:
        # print(resource_file)
