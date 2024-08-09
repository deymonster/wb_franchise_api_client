from typing import Optional, Union
from pydantic import BaseModel, Field


class APIConfig(BaseModel):
    """Model for API config
    """
    auth_base_path: str = ""
    base_path: str = ""
    verify: Union[bool, str] = True
    basic_token: Optional[str] = None

    def get_basic_token(self) -> Optional[str]:
        return self.basic_token

    def set_basic_token(self, value: str):
        self.basic_token = value


class HTTPException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"{status_code} {message}")

    def __str__(self):
        return f"{self.status_code} {self.message}"
