from fastapi import FastAPI, status, HTTPException
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
    result = utils.search_students(country, age)
    if result["status"] == False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error retrieving records!",
        )
    else:
        return result["data"]


@app.get(
    "/students/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.SingleStudentSearchResponse,
)
async def student_by_id(id: int):
    result = utils.search_students_by_id(id)
    if result["status"] == False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error retrieving record with id: {id}!",
        )
    else:
        return result["data"]


@app.post(
    "/students",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.StudentCreateResponse,
)
async def put_students(student: schemas.StudentCreate):
    result = utils.add_student(student)
    if result["status"] == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Error adding the record!",
        )
    else:
        return result["data"]


@app.patch("/students/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_student_by_id(id: int, student: Optional[schemas.StudentUpdate]):
    result = utils.update_by_id(id, student)
    if result["status"] == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Error updating record with id: {id}!",
        )


@app.delete("/students/{id}", status_code=status.HTTP_200_OK)
async def delete_student_by_id(id: int):
    result = utils.delete_by_id(id)
    if result["status"] == False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error deleting record with id: {id}!",
        )
