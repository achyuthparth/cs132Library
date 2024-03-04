from os import path
import json
import file_services as FS

class User:
    name : str
    email : str
    number : int
    id : int


class Patron(User):
    __password : str

class Librarian(User):
    __password : str
    
    @classmethod
    def create_patron(cls):
        return
    
    @classmethod
    def create_librarian(cls):
        return


class User_Encoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

class User_Encoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.toObject)

class User_File:
    def __init__(self, fileName = "User_List.json"):
        self.FileName = FS.CreateFilePath(fileName)

    def ReadFile(self):
        fileExists = path.exists(self.FileName)
        if fileExists:
            with open(self.FileName, 'r') as infile:
                json_object = json.load(infile, cls = User_Encoder)
        else:
            json_object = {}
        return json_object

    def WriteFile(self, vocabList):
        with open(self.FileName, "w") as outfile:
            json.dump(vocabList, outfile, cls = User_Encoder)
        return