from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    name: str
    email: str
    password: str

class UserGet(UserBase):
    class Config:
        from_attributes = True
