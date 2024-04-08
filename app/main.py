from fastapi import FastAPI, status
from . import schemas, utils
from typing import List
from typing import Optional


app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello Earth"}


@app.get(
    "/students",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.StudentsSearchResponse],
)
async def get_students(country: str = None, age: int = None):
    students = utils.search_students(country, age)
    return students


@app.get(
    "/students/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.SingleStudentSearchResponse,
)
async def student_by_id(id: int):
    student = utils.search_students_by_id(id)
    return student


@app.post(
    "/students",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.StudentCreateResponse,
)
async def put_students(student: schemas.StudentCreate):
    id = utils.add_student(student)
    return id


@app.patch("/students/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_student_by_id(id: int, student: Optional[schemas.StudentUpdate]):
    update_status = utils.update_by_id(id, student)
    return {"message": "Hello Earth"}


@app.delete("/students/{id}", status_code=status.HTTP_200_OK)
async def delete_student_by_id(id: int):
    delete_status = utils.delete_by_id(id)
    return {"message": "Hello Earth"}
