import os
import configparser

class Config:
    """
    Loads environment configuration from INI files.
    """

    _config = configparser.ConfigParser()

    @classmethod
    def _load_config(cls, file_path):
        """Helper method to load configuration file."""
        if os.path.exists(file_path):
            cls._config.read(file_path)
        else:
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

    @classmethod
    def load(cls):
        """Loads all required configurations."""
        user_path = os.environ.get('USERPROFILE', os.path.expanduser("~"))
        
        # Token config file
        token_file = os.path.join(user_path, "AppData", "kart", "tokensnibo_Geral.ini")
        cls._load_config(token_file)

        # Database config file
        db_file = os.path.join(user_path, "AppData", "kart", "configDWH_nibo.ini")
        cls._load_config(db_file)

    @classmethod
    def get_database_config(cls):
        """Retrieve database credentials."""
        return {
            'host': cls._config.get('database', 'host', fallback=None),
            'user': cls._config.get('database', 'user', fallback=None),
            'password': cls._config.get('database', 'password', fallback=None),
            'database': cls._config.get('database', 'database', fallback=None),
        }

    @classmethod
    def get_token(cls, key):
        """Retrieve a specific token from the 'credenciais' section."""
        return cls._config.get('credenciais', key, fallback=None)

# Load configurations at the module level
Config.load()
