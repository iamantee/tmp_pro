import os 
import ConfigParser

class Configuration(object):

    def __init__(self):
        pass

    """
        Load Configuration 
    """
    _CONFIG_FILE_NAME = 'config.ini'

    _current_dir_abs_path = os.path.dirname(os.path.abspath(__file__))
    _config_file_abs_path = os.path.join(_current_dir_abs_path, _CONFIG_FILE_NAME)
    
    _config = ConfigParser.ConfigParser()
    _config.read(_config_file_abs_path)

    @staticmethod
    def get_sections():
        try:
            return Configuration._config.sections()
        except:
            raise 

    @staticmethod
    def get_option(section, option):
        try:
            return Configuration._config.get(section, option)
        except: 
            raise


if __name__ == '__main__':
    config_section = 'file.reader.hkex.daily.quotations'
    config_option = 'ContentSectionCatPattern'
    print Configuration.get_sections()
    print Configuration.get_option(config_section, config_option)