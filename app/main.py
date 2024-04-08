from fastapi import FastAPI, status
from . import schemas

app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello Earth"}


@app.get("/students", status_code=status.HTTP_200_OK)
async def get_students():
    return {"message": "Hello Earth"}


@app.get("/students/{id}", status_code=status.HTTP_200_OK)
async def get_student_by_id(id: int):
    return {"message": "Hello Earth"}


@app.post(
    "/students",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.StudentResponse,
)
async def create_students(student: schemas.StudentCreate):
    return {"id": "Hello Earth"}


@app.patch("/students/{id}", status_code=status.HTTP_200_OK)
async def update_student_by_id(id: int):
    return {"message": "Hello Earth"}


@app.delete("/students/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student_by_id(id: int):
    return {"message": "Hello Earth"}
