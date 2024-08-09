from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    expires_in: int
    refresh_token: str
    token_type: str



