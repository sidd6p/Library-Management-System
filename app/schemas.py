from pydantic import BaseModel
from typing import Optional


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


class AddressOptional(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[AddressOptional] = None


class StudentCreateResponse(BaseModel):
    id: str
