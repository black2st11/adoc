from common.dto import BaseModel


class InSignupDTO(BaseModel):
    email: str
    password: str
    re_password: str

class InLoginDTO(BaseModel):
    email: str
    password: str
