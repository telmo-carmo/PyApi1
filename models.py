
from typing import Optional
from pydantic import BaseModel

# Pydantic model for task data
class ItemRequest(BaseModel):
    name: str
    price: float
    is_offer: bool

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    is_offer: bool

class LoginReq(BaseModel):
    uid: str
    pwd: str

class LoginResp(BaseModel):
    token: str      | None
    error: str      | None
    username: Optional[str]   =  None
