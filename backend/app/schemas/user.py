from fastapi_users import schemas
from pydantic import EmailStr, Field

class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str = Field(min_length=8)

    class Config:
        json_schema_extra = {
            'example': {
                'email': 'user@example.com',
                'password': 'strongpassword'
            }
        }
