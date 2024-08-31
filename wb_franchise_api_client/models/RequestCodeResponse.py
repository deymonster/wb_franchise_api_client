from pydantic import BaseModel


class RequestCodeResponse(BaseModel):
    isPush: bool
    isSuccess: bool
    sentToBell:  bool
    sentToNotifications: bool
    waitTimeout: int
