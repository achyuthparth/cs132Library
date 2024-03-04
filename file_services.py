import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

def CreateFilePath(fileName):
	filePath = os.path.join(BASE_DIR, fileName)
	print("Created File Path: " + filePath)
	return filePath