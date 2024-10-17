from pydantic_settings import BaseSettings
from pydantic import ValidationError

class Settings(BaseSettings):
    database_hostname: str
    database_username: str
    database_password: str
    database_port: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

try:
    settings = Settings()
except ValidationError as e:
    # Print the entire error details including input_value
    print(e.errors())  # this will show the full error details
    # If you specifically want to print the input_value
    for error in e.errors():
        if "input_value" in error:
            print("Input Value: ", error["input_value"])