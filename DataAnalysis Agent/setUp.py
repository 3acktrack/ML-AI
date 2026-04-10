def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
warnings.filterwarnings('ignore')

import configparser
import os
import logging
import ast

class Parser:
    def __init__(self, modelName):
        self.modelName = modelName
        self.configPath = self.getConfig()
        self.log = Log().getLogger()
        self.typed_data = {}
        
    def getConfig(self):
        if "llm.config" not in os.listdir():
            self.log.error("log file not present")
        else:
            return os.path.join(os.getcwd(), 'llm.config')
    
    def load_config(self):
    # Initialize the parser
        config = configparser.ConfigParser()
        
        # Check if file exists before reading
        if not os.path.exists(self.configPath):
            self.log.error(f"Error: {self.configPath} not found.")
            return None
        # code to check hash of config for security

        # Load the file
        config.read(self.configPath)
    
        """for section in config.sections():
            self.typed_data[section] = {}
            for key, value in config.items(section):
                try:
                    # ast.literal_eval handles lists, dicts, floats, ints, and bools
                    self.typed_data[section][key] = ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    # Fallback to string if it's not a valid Python literal
                    self.typed_data[section][key] = value
        return self.typed_data[self.modelName]"""
        return config
    
    
 

class Log:
    def __init__(self):
        self.logger = logging.getLogger("analysisAgentLogger")
        self.logger.setLevel(logging.DEBUG)  # Capture everything from DEBUG level up
        f_handler = logging.FileHandler('analysisApp.log')
        f_handler.setLevel(logging.DEBUG)      # File only records ERROR and above
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(log_format)
        self.logger.addHandler(f_handler)

    def getLogger(self):
        return self.logger
        
def unitTest():
    parser = Parser("openai")
    config = parser.load_config()
    log = Log()
    logger = log.getLogger()
    logger.info(config['openai']['systemPrompt'])
    print (config['openai']['systemPrompt'])
    
if __name__ == "__main__":
    unitTest()
    