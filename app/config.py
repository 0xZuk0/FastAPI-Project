from pydantic import BaseSettings

class Settings(BaseSettings) :
    database_hostname : str
    database_port : str
    database_password : str
    database_username : str
    database_name : str
    secret_key : str
    algorithm : str
    expire_time : int

    class Config :
        env_file = ".env"

settings = Settings()