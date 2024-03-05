import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

def create_file_path(file_name):
	filePath = os.path.join(BASE_DIR, file_name)
	print("Created File Path: " + filePath)
	return filePath

def create_file(file_name):
    file_path = create_file_path(file_name)
    with open(file_path, "w") as file_path:
        json.dump({}, file_path)
    return file_path