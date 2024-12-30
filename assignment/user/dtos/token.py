from common.dto import BaseModel
from user.models.user import User


class InGenerateTokenDto(BaseModel):
    user: User | None = None
    access_token: str | None = None
    refresh_token: str | None = None

class OutGenerateTokenDto(BaseModel):
    access_token: str
    refresh_token: str


