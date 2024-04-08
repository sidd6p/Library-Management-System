from fastapi import FastAPI, status, HTTPException, Depends
from . import schemas, utils
from .database import get_db
from typing import List
from typing import Optional

from pymongo.database import Database

app = FastAPI()


@app.get("/app-check", status_code=status.HTTP_200_OK)
async def app_check():
    return {"message": "Hello Earth"}


@app.get("/database-check", status_code=status.HTTP_200_OK)
async def db_check(db: Database = Depends(get_db)):
    try:
        db.command("ping")
        return {"message": "DB conected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to connect to the database.",
        )


@app.get(
    "/students",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.StudentsSearchResponse],
)
async def get_students(
    country: str = None, age: int = None, db: Database = Depends(get_db)
):
    try:
        result = await utils.search_students(db, country, age)
        if result["status"] == False:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["detail"],
            )
        else:
            return result["data"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.get(
    "/students/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.SingleStudentSearchResponse,
)
async def student_by_id(id: str, db: Database = Depends(get_db)):
    try:
        result = await utils.search_students_by_id(id, db)
        if result["status"] == False:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["detail"],
            )
        else:
            return result["data"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.post(
    "/students",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.StudentCreateResponse,
)
async def put_students(student: schemas.StudentCreate, db: Database = Depends(get_db)):
    try:
        result = await utils.add_student(student, db)
        if result["status"] == False:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["detail"],
            )
        else:
            return result["data"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.patch("/students/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_student_by_id(
    id: str, student: Optional[schemas.StudentUpdate], db: Database = Depends(get_db)
):
    try:
        result = await utils.update_by_id(id, student, db)
        if result["status"] == False:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=result["detail"],
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.delete("/students/{id}", status_code=status.HTTP_200_OK)
async def delete_student_by_id(id: str, db: Database = Depends(get_db)):
    try:
        result = await utils.delete_by_id(id, db)
        if result["status"] == False:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["detail"],
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
