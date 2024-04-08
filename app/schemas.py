from pydantic import BaseModel


class Address(BaseModel):
    city: str
    country: str


class StudentCreate(BaseModel):
    name: str
    age: int
    address: Address

    class Config:
        schema_extra = {
            "example": {
                "name": "Siddhartha",
                "age": 23,
                "address": {"city": "Jalaun", "country": "India"},
            }
        }


class StudentResponse(BaseModel):
    id: str
