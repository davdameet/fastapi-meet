from pydantic import BaseSettings
class Settings(BaseSettings):
    database_name:str
    database_password:str
    database_hostname:str
    database_port:str
    database_username:str
    secret_key:str
    access_token:int
    algorithm:str
    class Config:
        env_file=".env"
settings=Settings()