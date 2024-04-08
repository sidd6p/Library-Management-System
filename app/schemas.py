from pydantic import BaseModel


class StudentBaseModel(BaseModel):
    name: str
    age: int


class StudentsSearchResponse(StudentBaseModel):
    pass


class Address(BaseModel):
    city: str
    country: str


class SingleStudentSearchResponse(StudentBaseModel):
    address: Address


class StudentCreate(StudentBaseModel):
    address: Address

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
