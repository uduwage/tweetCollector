import os
from ConfigParser import SafeConfigParser

class FileLocator():

    def __init__(self):
        self.config = SafeConfigParser()
        self.script_dir = os.path.dirname(__file__)
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(self.script_dir, "../settings.cfg")
        self.config.read(self.config_file)

    def getTwitterTokens(self):
        """
        Construct the access token for twitter login
        :return: token a dictionary containing all the keys
        """
        tokens = {
            'CONSUMER_KEY' : self.config.get('twitter', 'consumer_key'),
            'CONSUMER_SECRET' : self.config.get('twitter', 'consumer_secret'),
            'ACCESS_KEY' : self.config.get('twitter', 'access_key'),
            'ACCESS_SECRET' : self.config.get('twitter', 'access_secret'),
        }
        return tokens

    def getFileLocations(self):
        """
        Construct dictionary with file locations
        :return: filelocations dictionary with file locations as values
        """
        fileLocations = {
            'ROOT_LOCATION' : os.path.abspath(os.path.join(os.getcwd(), os.pardir)),
            'OUTPUT_FOLDER': self.config.get('files', 'output_folder'),
            'LOG_FILE' : self.config.get('files', 'logfile'),
            'DATA_FOLDER' : self.config.get('files', 'data_folder'),
            'INPUT_FOLDER' : self.config.get('files', 'input_folder')
        }
        return fileLocations