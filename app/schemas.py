from pydantic import BaseModel


class Address(BaseModel):
    city: str
    country: str


class StudentBaseModel(BaseModel):
    name: str
    age: int


class StudentSearchResponse(StudentBaseModel):
    pass


class StudentCreate(StudentBaseModel):
    name: str
    age: int

    class Config:
        schema_extra = {
            "example": {
                "name": "Siddhartha",
                "age": 23,
                "address": {"city": "Jalaun", "country": "India"},
            }
        }


class StudentCreateResponse(BaseModel):
    id: str
