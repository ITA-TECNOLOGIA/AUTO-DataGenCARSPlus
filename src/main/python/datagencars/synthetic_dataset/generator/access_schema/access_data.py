from configparser import ConfigParser


class AccessData:

    '''
    Parent class that allows access to the properties of a string with file information.
    @author Maria del Carmen Rodriguez-Hernandez 
    '''    

    def __init__(self, file_str):        
        self.file_parser = ConfigParser()
        self.file_parser.read_string(file_str)
        print(f"AccessGenerationConfig: {self.file_parser.sections()}")  # Added print statement for debugging
