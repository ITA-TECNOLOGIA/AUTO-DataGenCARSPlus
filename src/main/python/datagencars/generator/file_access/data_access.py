from configparser import SafeConfigParser


class DataAccess:

    '''
    Parent class that allows access to the properties of a file.
    @author Maria del Carmen Rodriguez-Hernandez 
    '''

    def __init__(self, file_path):
        self.file_path = file_path     
        self.file_parser = SafeConfigParser()        
        with open(file_path, 'r') as g:
            self.file_parser.readfp(g)
